from __future__ import annotations

import logging

_LOGGER = logging.getLogger(__name__)

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AvalonMinerCoordinator
from .avalon_api import AsyncAvalonAPI
from .const import DOMAIN


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

    _attr_has_entity_name = True
    _attr_translation_key = "fan_speed"

    _attr_native_min_value = 15
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"
    _attr_icon = "mdi:fan"

    def __init__(
        self,
        coordinator: AvalonMinerCoordinator,
        api: AsyncAvalonAPI,
        entry_id: str,
        device_info: dict,
    ):
        super().__init__(coordinator)

        self.api = api
        self._fan_speed = None

        self._attr_unique_id = f"{entry_id}_fan_speed"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        if self._fan_speed is not None:
            return self._fan_speed

        estats = self.coordinator.data.get("estats", {})
        fans = estats.get("fans", {})

        return fans.get("FanR", 100)

    async def async_set_native_value(self, value: float) -> None:
        value = int(value)

        await self.api.set_fan_speed(value)

        # Optimistisches Update
        self._fan_speed = value
        self.async_write_ha_state()

        # Miner später abfragen
        await self.coordinator.async_request_refresh()
