# custom_components/avalon_nano3s/select.py
from __future__ import annotations

import logging
import time

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AvalonMinerCoordinator
from .avalon_api import AsyncAvalonAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Pool-Wechsel: Der Miner hasht nach dem Umschalten noch ca. 2 Minuten mit
# Arbeit des alten Pools weiter, der neue Pool bestätigt erst danach den
# ersten Share. So lange gilt der Wechsel als "laufend" (Attribut switching).
POOL_SWITCH_TIMEOUT = 300  # Sekunden, danach wird "switching" in jedem Fall beendet
POOL_SWITCH_GRACE = 15     # Sekunden, in denen noch veraltete Daten ignoriert werden

# =========================
# Workmode Mapping
# =========================
WORK_MODES = {
    "Low": 0,
    "Mid": 1,
    "High": 2,
}
REVERSE_WORK_MODES = {v: k for k, v in WORK_MODES.items()}

# =========================
# LED Effekt Mapping
# =========================
LED_EFFECTS = {
    "LED_off": 0,
    "Stay": 1,
    "Flash": 2,
    "Breathing": 3,
    "Loop": 4,
}
REVERSE_LED_EFFECTS = {v: k for k, v in LED_EFFECTS.items()}

# =========================
# Pool Mapping
# =========================
POOL_INDEX = {
    "Pool 1": 0,
    "Pool 2": 1,
    "Pool 3": 2,
}
REVERSE_POOL_INDEX = {v: k for k, v in POOL_INDEX.items()}

# =========================
# Setup Entry
# =========================
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: AvalonMinerCoordinator = data["coordinator"]
    api: AsyncAvalonAPI = data["api"]
    device_info = data["device_info"]

    async_add_entities(
        [
            AvalonWorkModeSelect(coordinator, api, entry.entry_id, device_info),
            AvalonLedEffectSelect(coordinator, api, entry.entry_id, device_info),
            AvalonPoolSelect(coordinator, api, entry.entry_id, device_info),
        ]
    )

# =========================
# Workmode Select
# =========================
class AvalonWorkModeSelect(CoordinatorEntity, SelectEntity):
    """SelectEntity für den Workmode des Avalon Nano 3S."""

    _attr_has_entity_name = True
    _attr_options = list(WORK_MODES.keys())
    _attr_translation_key = "workmode"

    def __init__(
        self,
        coordinator: AvalonMinerCoordinator,
        api: AsyncAvalonAPI,
        entry_id: str,
        device_info: dict,
    ):
        super().__init__(coordinator)
        self.api = api

        self._attr_unique_id = f"{entry_id}_workmode"
        self._attr_device_info = device_info

    @property
    def current_option(self) -> str:
        estats = self.coordinator.data.get("estats", {})
        workmode_val = estats.get("WORKMODE")
        try:
            return REVERSE_WORK_MODES[int(workmode_val)]
        except (TypeError, ValueError, KeyError):
            return "Low"

    async def async_select_option(self, option: str) -> None:
        level = WORK_MODES.get(option)
        if level is None:
            _LOGGER.warning("Unbekannter Workmode: %s", option)
            return

        await self.api.set_workmode(level)
        await self.coordinator.async_request_refresh()


# =========================
# LED Effekt Select
# =========================
class AvalonLedEffectSelect(CoordinatorEntity, SelectEntity):
    """SelectEntity für die LED-Effekte des Avalon Nano 3S."""

    _attr_has_entity_name = True
    _attr_options = list(LED_EFFECTS.keys())
    _attr_translation_key = "led_effect"

    def __init__(
        self,
        coordinator: AvalonMinerCoordinator,
        api: AsyncAvalonAPI,
        entry_id: str,
        device_info: dict,
    ):
        super().__init__(coordinator)
        self.api = api

        self._attr_unique_id = f"{entry_id}_led_effect"
        self._attr_device_info = device_info

    @property
    def current_option(self) -> str:
        estats = self.coordinator.data.get("estats", {})
        led_user = estats.get("led", {}).get("LEDUser", {})
        effect_val = led_user.get("Effect", 1)
        return REVERSE_LED_EFFECTS.get(effect_val, "Stay")

    async def async_select_option(self, option: str) -> None:
        effect_id = LED_EFFECTS.get(option)
        if effect_id is None:
            _LOGGER.warning("Unbekannter LED-Effekt: %s", option)
            return

        led_user = self.coordinator.data.get("estats", {}).get("led", {}).get("LEDUser", {})
        brightness = led_user.get("Brightness", 100)
        color_temp = led_user.get("ColorTemp", 50)
        r = led_user.get("R", 255)
        g = led_user.get("G", 255)
        b = led_user.get("B", 255)

        await self.api.set_led(effect_id, brightness, color_temp, r, g, b)
        await self.coordinator.async_request_refresh()

# =========================
# Pool-Switch Select
# =========================
def _to_int(value, default=-1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class AvalonPoolSelect(CoordinatorEntity, SelectEntity):
    """Pool switching via CGMiner API."""

    _attr_has_entity_name = True
    _attr_options = ["Pool 1", "Pool 2", "Pool 3"]
    _attr_translation_key = "pool"

    def __init__(self, coordinator, api, entry_id, device_info):
        super().__init__(coordinator)
        self.api = api
        self._attr_unique_id = f"{entry_id}_pool_select"
        self._attr_device_info = device_info

        # Laufender Pool-Wechsel (None = kein Wechsel aktiv)
        self._switch_target = None
        self._switch_baseline = 0
        self._switch_started = 0.0

    def _safe_pools(self):
        """Never fail during setup."""
        try:
            data = getattr(self.coordinator, "data", None)
            if not data:
                return {}

            pools = data.get("pools")
            if not isinstance(pools, dict):
                return {}

            return pools
        except Exception:
            return {}

    def _pool_by_number(self, pool_nr):
        for pool in self._safe_pools().values():
            if isinstance(pool, dict) and _to_int(pool.get("POOL")) == pool_nr:
                return pool
        return None

    def _active_pool_nr(self):
        """Nummer (0-2) des aktiven Pools, None wenn nicht ermittelbar.

        Strategie ist Failover: Der aktive Pool ist der mit Priority 0.
        switchpool setzt den gewählten Pool sofort auf Priority 0. "Stratum
        Active" taugt dafür nicht, weil kurz nach einem Wechsel beide Pools
        als aktiv gemeldet werden.
        """
        pools = self._safe_pools()

        for pool in pools.values():
            if isinstance(pool, dict) and _to_int(pool.get("Priority")) == 0:
                pool_nr = _to_int(pool.get("POOL"))
                if pool_nr >= 0:
                    return pool_nr

        # Fallback (Priority nicht vorhanden): bisheriges Verfahren
        # Pool 3 hat Vorrang vor Pool 2, Pool 2 vor Pool 1.
        active = {}
        for pool in pools.values():
            if not isinstance(pool, dict):
                continue
            active[_to_int(pool.get("POOL"))] = (
                str(pool.get("Stratum Active", "")).lower() == "true"
            )

        for pool_nr in (2, 1, 0):
            if active.get(pool_nr):
                return pool_nr

        return None

    @property
    def current_option(self) -> str:
        try:
            pool_nr = self._active_pool_nr()
            if pool_nr in (0, 1, 2):
                return f"Pool {pool_nr + 1}"
            return "Pool 1"

        except Exception:
            return "Pool 1"

    @property
    def extra_state_attributes(self):
        return {"switching": self._switch_target is not None}

    def _refresh_switching(self) -> None:
        """Laufenden Wechsel beenden, sobald er abgeschlossen oder hinfällig ist."""
        if self._switch_target is None:
            return

        elapsed = time.monotonic() - self._switch_started

        if elapsed > POOL_SWITCH_TIMEOUT:
            self._switch_target = None
            return

        # Miner nicht erreichbar / keine Daten: nichts entscheiden
        if not self.coordinator.last_update_success or not self._safe_pools():
            return

        # Direkt nach dem Befehl können noch veraltete Daten eintreffen
        if elapsed < POOL_SWITCH_GRACE:
            return

        # Wechsel wurde überschrieben (z. B. Neustart setzt Prioritäten zurück)
        if self._active_pool_nr() != self._switch_target:
            self._switch_target = None
            return

        # Neuer Pool hat den ersten Share bestätigt -> Wechsel abgeschlossen
        pool = self._pool_by_number(self._switch_target)
        if pool and _to_int(pool.get("Accepted"), 0) > self._switch_baseline:
            self._switch_target = None

    @callback
    def _handle_coordinator_update(self) -> None:
        self._refresh_switching()
        super()._handle_coordinator_update()

    async def async_select_option(self, option: str) -> None:
        mapping = {"Pool 1": 0, "Pool 2": 1, "Pool 3": 2}

        idx = mapping.get(option)
        if idx is None:
            return

        already_active = self._active_pool_nr() == idx

        result = await self.api.switch_pool(idx)

        if result.get("success") and not already_active:
            pool = self._pool_by_number(idx)
            self._switch_baseline = _to_int(
                pool.get("Accepted"), 0
            ) if pool else 0
            self._switch_target = idx
            self._switch_started = time.monotonic()
            self.async_write_ha_state()

        await self.coordinator.async_request_refresh()
