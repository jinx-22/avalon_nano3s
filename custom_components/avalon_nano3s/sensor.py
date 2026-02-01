# custom_components/avalon_nano3s/sensor.py
from __future__ import annotations
import logging
from datetime import datetime, timezone

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PERCENTAGE = "%"

# ===========================
# Sensor-Keys
# ===========================
VISIBLE_VERSION_KEYS = {
    "MODEL",
    "CGMiner",
    "LVERSION",
}
VISIBLE_SUMMARY_KEYS = {
    "MHS av",
    "MHS 5s",
    "MHS 5m",
    "MHS 15m",
    "Found Blocks",
    "Accepted",
    "Rejected",
    "Utility",
    "Elapsed",
    "Best Share",
    "Device Rejected%",
    "Pool Rejected%",
    "Total MH",
    "Device Hardware%",
}
VISIBLE_ESTATS_KEYS = {
    "OTemp",
    "TAvg",
    "TarT",
    "Fan1",
    "FanR",
    "DH",
    "GHSspd",
    "GHSmm",
    "Freq",
    "MTavg",
    "PS_HashboardVoltage",
    "PS_Ping",
    "PS_Power",
}
VISIBLE_POOLS_DIAG = {"URL", "User", "Password", "Stratum URL", "Status", "Work Difficulty"}
VISIBLE_POOLS_KEYS = {
    "Last Share Time",
    "Diff1 Shares",
    "Pool Rejected%",
    "Pool Stale%",
    "Current Block Height",
    "Stratum Active",
    "Stratum Difficulty",
}

# ===============================
# Sensor-Konfiguration
# ===============================
SENSOR_CONFIG = {
    "ITemp": (SensorDeviceClass.TEMPERATURE, "°C", SensorStateClass.MEASUREMENT, lambda v: round(float(v), 1)),
    "OTemp": (SensorDeviceClass.TEMPERATURE, "°C", SensorStateClass.MEASUREMENT, lambda v: round(float(v), 1)),
    "TMax": (SensorDeviceClass.TEMPERATURE, "°C", SensorStateClass.MEASUREMENT, lambda v: round(float(v), 1)),
    "TAvg": (SensorDeviceClass.TEMPERATURE, "°C", SensorStateClass.MEASUREMENT, lambda v: round(float(v), 1)),
    "TarT": (SensorDeviceClass.TEMPERATURE, "°C", SensorStateClass.MEASUREMENT, lambda v: round(float(v), 1)),
    "MTmax": (SensorDeviceClass.TEMPERATURE, "°C", SensorStateClass.MEASUREMENT, lambda v: round(float(v), 1)),
    "MTavg": (SensorDeviceClass.TEMPERATURE, "°C", SensorStateClass.MEASUREMENT, lambda v: round(float(v), 1)),
    "Fan1": (None, "RPM", SensorStateClass.MEASUREMENT, lambda v: int(float(v))),
    "FanR": (None, PERCENTAGE, SensorStateClass.MEASUREMENT, lambda v: round(float(str(v).replace("%", "")), 1)),
    "PS_Power": (SensorDeviceClass.POWER, "W", SensorStateClass.MEASUREMENT, lambda v: int(v)),
    "PS_HashboardVoltage": (None, "mV", None, lambda v: int(v)),
    "PS_Ping": (None, "ms", None, lambda v: int(v)),
    "GHSspd": (None, "TH/s", SensorStateClass.MEASUREMENT, lambda v: round(float(v) / 1000, 3)),
    "GHSavg": (None, "TH/s", SensorStateClass.MEASUREMENT, lambda v: round(float(v) / 1000, 3)),
    "GHSmm": (None, "TH/s", SensorStateClass.MEASUREMENT, lambda v: round(float(v) / 1000, 3)),
    "Freq": (None, "MHz", None, lambda v: round(float(v), 2)),
    "MHS av": (None, "TH/s", SensorStateClass.MEASUREMENT, lambda v: round(float(v) / 1_000_000, 3)),
    "MHS 5s": (None, "TH/s", SensorStateClass.MEASUREMENT, lambda v: round(float(v) / 1_000_000, 3)),
    "MHS 5m": (None, "TH/s", SensorStateClass.MEASUREMENT, lambda v: round(float(v) / 1_000_000, 3)),
    "MHS 15m": (None, "TH/s", SensorStateClass.MEASUREMENT, lambda v: round(float(v) / 1_000_000, 3)),
    "Total MH": (None, "PH", SensorStateClass.TOTAL_INCREASING, lambda v: round(v / 1_000_000_000, 3)),
    "Device Rejected%": (None, PERCENTAGE, SensorStateClass.MEASUREMENT, lambda v: round(float(v), 2)),
    "Pool Rejected%": (None, PERCENTAGE, SensorStateClass.MEASUREMENT, lambda v: round(float(v), 2)),
    "Device Hardware%": (None, PERCENTAGE, SensorStateClass.MEASUREMENT, lambda v: round(float(v), 2)),
    "Pool Stale%": (None, PERCENTAGE, SensorStateClass.MEASUREMENT, lambda v: round(float(v), 2)),
    "Accepted": (None, None, SensorStateClass.TOTAL_INCREASING, lambda v: int(float(v))),
    "Rejected": (None, None, SensorStateClass.TOTAL_INCREASING, lambda v: int(float(v))),
    "Best Share": (None, None, SensorStateClass.TOTAL_INCREASING, lambda v: int(float(v))),
    "Found Blocks": (None, "Blocks", SensorStateClass.TOTAL_INCREASING, lambda v: int(float(v))),
    "Current Block Height": (None, None, SensorStateClass.TOTAL_INCREASING, lambda v: int(float(v))),
    "Diff1 Shares": (None, None, SensorStateClass.TOTAL_INCREASING, lambda v: int(float(v))),
    "Stratum Difficulty": (None, None, SensorStateClass.TOTAL_INCREASING, lambda v: int(float(v))),
    "Activation": (None, None, None, lambda v: int(float(v))),
    "MEMFREE": (None, "KiB", SensorStateClass.MEASUREMENT, lambda v: int(float(v))),
}

# ===============================
# Sensor-Klasse
# ===============================

class AvalonSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator,
        entry_id,
        api_type,
        section_name,
        key,
        enabled_default,
        category,
        device_info,
    ):
        super().__init__(coordinator)

        # WICHTIG: speichern für native_value
        self._api_type = api_type
        self._section_name = section_name
        self._key = key.strip()

        raw = self._key
        norm = raw.replace("%", "").lower().replace(" ", "_")

        translation_key = f"{section_name}_{norm}" if api_type == "pools" else norm

        # HA 2026 offizieller Fallback
        self.entity_description = SensorEntityDescription(
            key=norm,
            translation_key=translation_key,
            name=raw,   # ← RAW NAME FALLBACK
            entity_category=category,
        )

        self._attr_has_entity_name = True

        self._attr_unique_id = f"{entry_id}_{api_type}_{section_name}_{norm}"
        self._attr_device_info = device_info
        self._attr_entity_registry_enabled_default = enabled_default

        config = SENSOR_CONFIG.get(self._key)
        if config:
            device_class, unit, state_class, _ = config
            if device_class:
                self._attr_device_class = device_class
            if unit:
                self._attr_native_unit_of_measurement = unit
            if state_class:
                self._attr_state_class = state_class


    @property
    def native_value(self):
        try:
            data = self.coordinator.data.get(self._api_type, {})
            section = data.get(self._section_name, {})
            value = section.get(self._key)
            if value is None:
                return None

            raw_value = value

            # -----------------------------
            # PING aktualisierung
            # -----------------------------
            if self._key == "PS_Ping":
                try:
                    return round(float(str(value).strip()), 1)
                except Exception as e:
                    _LOGGER.debug("PS_Ping konnte nicht konvertiert werden: %s (raw=%s)", e, value)
                    return None

            # Spezieller Fall: Last Share Time → Timestamp → Datum/Uhrzeit
            if self._key == "Last Share Time":
                try:
                    seconds = int(float(raw_value))
                    if seconds <= 0:
                        return "no connection"

                    dt = datetime.fromtimestamp(seconds, tz=timezone.utc).astimezone()
                    return dt.strftime("%H:%M – %d.%m.%Y")
                except (ValueError, TypeError, OverflowError) as e:
                    _LOGGER.debug("Ungültiger Timestamp in Last Share Time: %s (%s)", raw_value, e)
                    return f"Ungültig ({raw_value})"

            # Spezieller Fall Elapsed
            if self._key.lower() == "elapsed":
                try:
                    total_seconds = int(float(raw_value))
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    return f"{hours}h {minutes:02d}m {seconds:02d}s"
                except Exception as e:
                    _LOGGER.debug("Fehler beim Formatieren von Elapsed: %s", e)
                    return str(raw_value)

            # Standard-Konverter
            config = SENSOR_CONFIG.get(self._key)
            if config:
                _, _, _, converter = config
                return converter(raw_value)

            try:
                return float(raw_value)
            except:
                return str(raw_value)

        except Exception as e:
            _LOGGER.debug("Fehler in native_value für Sensor %s: %s", self._attr_unique_id, e)
            return None

    @property
    def extra_state_attributes(self):
        attrs = {"last_polled": datetime.now().isoformat()}

        try:
            data = self.coordinator.data.get(self._api_type, {})
            section = data.get(self._section_name, {})
            raw_value = section.get(self._key)

            if self._key == "Last Share Time" and raw_value is not None:
                try:
                    seconds = int(float(raw_value))
                    attrs["raw_seconds"] = seconds
                    if seconds > 0:
                        dt = datetime.fromtimestamp(seconds, tz=timezone.utc).astimezone()
                        attrs["last_share_iso"] = dt.isoformat()
                except Exception as e:
                    _LOGGER.debug("Fehler beim Parsen raw_seconds für Last Share Time: %s", e)

            if self._key.lower() == "elapsed":
                try:
                    s = int(float(raw_value or 0))
                    attrs["formatted"] = f"{s//3600}h {(s%3600)//60:02d}m {s%60:02d}s"
                    attrs["total_seconds"] = s
                except Exception as e:
                    _LOGGER.debug("Fehler beim Formatieren Elapsed-Attribute: %s", e)

            return attrs

        except Exception as e:
            _LOGGER.debug("Fehler in extra_state_attributes für Sensor %s: %s", self._attr_unique_id, e)
            return attrs

# ===============================
# Setup Entry
# ===============================
async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator = data["coordinator"]
    device_info = data["device_info"]

    sensors = []

    def add_sensors(api_type, visible_keys, category=None):
        api_data = coordinator.data.get(api_type, {})
        for section_name, section_values in api_data.items():
            if not isinstance(section_values, dict):
                continue

            for key in section_values.keys():
                enabled = key in visible_keys

                sensors.append(
                    AvalonSensor(
                        coordinator,
                        entry.entry_id,
                        api_type,
                        section_name,
                        key,
                        enabled,
                        category,
                        device_info,
                    )
                )

    add_sensors("version", VISIBLE_VERSION_KEYS, EntityCategory.DIAGNOSTIC)
    add_sensors("summary", VISIBLE_SUMMARY_KEYS)
    add_sensors("estats", VISIBLE_ESTATS_KEYS)

    pools = coordinator.data.get("pools", {})
    for pool_id in ("p1", "p2", "p3"):
        pool_data = pools.get(pool_id, {})
        if not pool_data:
            continue

        for key in pool_data.keys():
            if pool_id == "p1":
                enabled_default = key in (VISIBLE_POOLS_KEYS | VISIBLE_POOLS_DIAG)
            else:
                enabled_default = key in VISIBLE_POOLS_DIAG

            category = EntityCategory.DIAGNOSTIC if key in VISIBLE_POOLS_DIAG else None

            sensors.append(
                AvalonSensor(
                    coordinator,
                    entry.entry_id,
                    "pools",
                    pool_id,
                    key,
                    enabled_default,
                    category,
                    device_info,
                )
            )

    async_add_entities(sensors)
