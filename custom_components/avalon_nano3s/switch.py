from homeassistant.components.switch import SwitchEntity
from .const import SWITCH_TYPES

class AvalonNano3SPowerSwitch(SwitchEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._name = SWITCH_TYPES["power_mode"]
        self._is_on = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.set_power_mode(1)
        self._is_on = True

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.set_power_mode(0)
        self._is_on = False