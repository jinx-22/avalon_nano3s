from __future__ import annotations
import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST, CONF_PORT, CONF_TIMEOUT
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryNotReady
from .avalon_api import AsyncAvalonAPI
from .const import DOMAIN, CONF_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SELECT,
    Platform.BUTTON,
    Platform.LIGHT,
]


class AvalonMinerCoordinator(DataUpdateCoordinator[dict]):
    """Data coordinator für Avalon Nano 3S"""

    def __init__(self, hass: HomeAssistant, api: AsyncAvalonAPI, update_interval: timedelta) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Avalon Nano 3S",
            update_interval=update_interval,
        )
        self.api = api

    async def _async_update_data(self) -> dict | None:
        """Fetch data from API – minimales Logging, HA-konform"""
        try:
            return {
                "version": await self.api.version(),
                "summary": await self.api.summary(),
                "stats": await self.api.stats(),
                "estats": await self.api.estats(),
                "devs": await self.api.devs(),
                "pools": await self.api.pools(),
            }
        except Exception as err:
            # Danach nur debug (kein Spam)
            if self.last_update_success:
                _LOGGER.warning("Update failed: %s", err)
            else:
                _LOGGER.debug("Update failed: %s", err)

            raise UpdateFailed(err) from err


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    update_interval_sec = entry.options.get(
        CONF_UPDATE_INTERVAL,
        entry.data.get(CONF_UPDATE_INTERVAL, 10),
    )

    api = AsyncAvalonAPI(
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
        entry.data[CONF_TIMEOUT],
    )

    coordinator = AvalonMinerCoordinator(
        hass,
        api,
        timedelta(seconds=update_interval_sec),
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error("Initial setup failed: %s", err)
        raise ConfigEntryNotReady from err

    device_info = {
        "identifiers": {(DOMAIN, entry.data[CONF_HOST])},
        "name": "Avalon Nano 3S",
        "manufacturer": "Canaan",
        "model": "Nano 3S",
    }
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
        "device_info": device_info,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok