# custom_components/avalon_nano3s/select.py
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AvalonMinerCoordinator
from .avalon_api import AsyncAvalonAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

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
