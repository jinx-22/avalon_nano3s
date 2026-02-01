from __future__ import annotations
from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator = data["coordinator"]
    api = data["api"]
    device_info = data["device_info"]

    async_add_entities(
        [
            AvalonLedLight(coordinator, api, entry.entry_id, device_info),
        ]
    )


# =========================
# LED Light Entity
# =========================
class AvalonLedLight(CoordinatorEntity, LightEntity):
    """Avalon Nano 3S LED – ON/OFF, Brightness & Palette (firmware-kompatibel)."""

    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB
    _attr_has_entity_name = True
    _attr_translation_key = "led_color"   # <-- Übersetzungsschlüssel

    def __init__(
        self,
        coordinator,
        api,
        entry_id: str,
        device_info: dict,
    ):
        super().__init__(coordinator)
        self.api = api
        
        self._attr_unique_id = f"{entry_id}_led"
        self._attr_device_info = device_info

        # Standardwerte
        self._attr_is_on = False
        self._attr_brightness = 128
        self._attr_rgb_color = (255, 255, 255)

        # Basisfarbe für Palette
        self._base_rgb_color = (255, 255, 255)

    # =========================
    # Firmware-kompatible RGB-Berechnung
    # =========================
    def _firmware_scale_rgb(self, base_rgb, brightness_ha):
        """Berechnet RGB wie die Firmware: 5–100 %, mindestens ein Kanal >= 13."""
        percent = max(5, round((brightness_ha / 255) * 100))

        r, g, b = base_rgb
        r = round(r * percent / 100)
        g = round(g * percent / 100)
        b = round(b * percent / 100)

        # Mindestens ein Kanal >= 13
        if r < 13 and g < 13 and b < 13:
            if r >= g and r >= b:
                r = 13
            elif g >= r and g >= b:
                g = 13
            else:
                b = 13

        return r, g, b, percent

    # =========================
    # Coordinator Update
    # =========================
    def _handle_coordinator_update(self) -> None:
        led = self.coordinator.data.get("estats", {}).get("led", {})
        user = led.get("LEDUser", {})

        if not isinstance(user, dict):
            return

        effect = user.get("Effect", 0)

        # OFF
        if effect == 0:
            self._attr_is_on = False
            self._attr_brightness = 0
            self._attr_rgb_color = (0, 0, 0)
            self.async_write_ha_state()
            return

        # ON (Effect = 1)
        self._attr_is_on = True

        bright_fw = user.get("Brightness", 100)
        self._attr_brightness = round((bright_fw / 100) * 255)

        # RGB Basis rekonstruieren
        r_fw = user.get("R", 255)
        g_fw = user.get("G", 255)
        b_fw = user.get("B", 255)

        if bright_fw > 0:
            scale = 255 / max(1, round((bright_fw / 100) * 255))
            self._base_rgb_color = (
                min(255, round(r_fw * scale)),
                min(255, round(g_fw * scale)),
                min(255, round(b_fw * scale)),
            )

        self._attr_rgb_color = (r_fw, g_fw, b_fw)

        self.async_write_ha_state()

    # =========================
    # Einschalten / Brightness / Palette
    # =========================
    async def async_turn_on(self, **kwargs):
        # Palette (RGB) separat behandeln
        if "rgb_color" in kwargs:
            self._base_rgb_color = kwargs["rgb_color"]

            r, g, b, percent = self._firmware_scale_rgb(
                self._base_rgb_color, self._attr_brightness
            )

            self._attr_rgb_color = (r, g, b)

            await self.api.set_led(1, percent, 50, r, g, b)

            self.async_write_ha_state()
            return

        # Helligkeit ändern (Slider)
        if "brightness" in kwargs:
            self._attr_brightness = kwargs["brightness"]
        elif self._attr_brightness == 0:
            self._attr_brightness = 128

        r, g, b, percent = self._firmware_scale_rgb(
            self._base_rgb_color, self._attr_brightness
        )

        await self.api.set_led(1, percent, 50, r, g, b)

        self._attr_is_on = True
        self._attr_rgb_color = (r, g, b)

        self.async_write_ha_state()

    # =========================
    # Ausschalten
    # =========================
    async def async_turn_off(self, **kwargs):
        await self.api.set_led(0, 5, 50, 0, 0, 0)

        self._attr_is_on = False
        self._attr_brightness = 0

        self.async_write_ha_state()
