from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta
import asyncio
import logging
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class AvalonNano3SCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name="Avalon Nano 3S",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.api.get_dashboard)