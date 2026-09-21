from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_TIMEOUT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .avalon_api import AsyncAvalonAPI
from .const import CONF_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SELECT,
    Platform.BUTTON,
    Platform.LIGHT,
    Platform.NUMBER,
]


class AvalonMinerCoordinator(DataUpdateCoordinator[dict]):
    """Data coordinator for Avalon Nano 3S."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: AsyncAvalonAPI,
        update_interval: timedelta,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Avalon Nano 3S",
            update_interval=update_interval,
        )
        self.api = api

    async def _async_update_data(self) -> dict:
        """Fetch data from the Avalon Nano 3S API."""

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
            # UpdateFailed is intentionally handled by
            # DataUpdateCoordinator. This causes coordinator
            # entities to become unavailable until the API
            # becomes reachable again.
            raise UpdateFailed(
                f"Avalon Nano 3S API unavailable: {err}"
            ) from err


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Avalon Nano 3S from a config entry."""

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

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Avalon Nano 3S."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
