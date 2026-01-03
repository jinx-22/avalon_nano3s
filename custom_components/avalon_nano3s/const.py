DOMAIN = "avalon_nano3s"
DEFAULT_SCAN_INTERVAL = 15

CONF_HOST = "host"
CONF_PASSWORD = "password"
CONF_NAME = "name"

SENSOR_TYPES = {
    "realtime_hash": ["Hashrate (Realtime)", "MH/s"],
    "average_hash": ["Hashrate (Average)", "MH/s"],
    "accepted": ["Accepted Shares", "shares"],
    "reject": ["Rejected Shares", "shares"],
    "rejected_percentage": ["Rejected %", "%"],
    "fan_status": ["Fan RPM", "RPM"],
    "power": ["Power Usage", "W"],
    "asic_status": ["ASIC Status", "status"],
    "ping": ["Ping", "ms"],
    "pool_status": ["Pool Status", "status"]
}

SWITCH_TYPES = {
    "power_mode": "Power Mode"
}