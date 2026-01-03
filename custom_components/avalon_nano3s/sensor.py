from homeassistant.helpers.entity import Entity
from .const import SENSOR_TYPES

class AvalonNano3SSensor(Entity):
    def __init__(self, coordinator, sensor_type):
        self.coordinator = coordinator
        self.type = sensor_type
        self._name = SENSOR_TYPES[sensor_type][0]
        self._unit = SENSOR_TYPES[sensor_type][1]
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        data = await self.coordinator.async_request_refresh()
        self._state = data.get(self.type)