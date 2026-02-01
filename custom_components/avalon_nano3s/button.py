# custom_components/avalon_nano3s/button.py
from __future__ import annotations
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import AvalonMinerCoordinator
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .avalon_api import AsyncAvalonAPI
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: AvalonMinerCoordinator = data["coordinator"]
    api: AsyncAvalonAPI = data["api"]
    entities = [
        AvalonRebootButton(coordinator, entry, api),
    ]
    async_add_entities(entities)

class AvalonBaseButton(CoordinatorEntity, ButtonEntity):
    def __init__(
        self,
        coordinator: AvalonMinerCoordinator,
        entry: ConfigEntry,
        api: AsyncAvalonAPI,
        translation_key: str,
    ) -> None:
        super().__init__(coordinator)  # muss zuerst CoordinatorEntity initialisieren

        self.api = api
        self._attr_translation_key = translation_key
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{entry.entry_id}_{translation_key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data[CONF_HOST])},
            "name": "Avalon Nano 3S",        # Device-Name muss hier gesetzt werden
            "manufacturer": "Canaan",
            "model": "Nano 3S",
        }


class AvalonRebootButton(AvalonBaseButton):
    def __init__(self, coordinator: AvalonMinerCoordinator, entry: ConfigEntry, api: AsyncAvalonAPI):
        super().__init__(coordinator, entry, api, translation_key="reboot")

    async def async_press(self) -> None:
        try:
            result = await self.api.reboot()
            if not result.get("success", False):
                _LOGGER.error("Reboot failed: %s", result.get("message"))
        except Exception as err:
            _LOGGER.error("Exception during reboot: %s", err)
        finally:
            await self.coordinator.async_request_refresh()