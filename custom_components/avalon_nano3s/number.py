from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AvalonMinerCoordinator
from .avalon_api import AsyncAvalonAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


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
            AvalonFanSpeedNumber(
                coordinator,
                api,
                entry.entry_id,
                device_info,
            )
        ]
    )


class AvalonFanSpeedNumber(CoordinatorEntity, NumberEntity):
    """Number entity for Avalon Nano 3S fan speed."""

    _attr_has_entity_name = True
    _attr_translation_key = "fan_speed"
    _attr_native_min_value = 15
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"
    _attr_icon = "mdi:fan"
    _attr_mode = NumberMode.BOX  # Eingabefeld mit + / - statt Slider

    def __init__(
        self,
        coordinator: AvalonMinerCoordinator,
        api: AsyncAvalonAPI,
        entry_id: str,
        device_info: dict,
    ) -> None:
        super().__init__(coordinator)
        self.api = api
        self._fan_speed: int | None = None
        self._attr_unique_id = f"{entry_id}_fan_speed"
        self._attr_device_info = device_info

    @property
    def native_value(self) -> float | None:
        """Return the current fan speed."""
        if self._fan_speed is not None:
            return self._fan_speed

        estats = self.coordinator.data.get("estats", {})
        fans = estats.get("fans", {})
        return fans.get("FanR", 100)

    async def async_set_native_value(self, value: float) -> None:
        """Set the fan speed."""
        value = int(value)
        await self.api.set_fan_speed(value)

        # Optimistisches Update
        self._fan_speed = value
        self.async_write_ha_state()

        # Miner später abfragen
        await self.coordinator.async_request_refresh()
