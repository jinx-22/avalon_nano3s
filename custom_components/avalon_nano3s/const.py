# custom_components/avalon_nano3s/const.py
"""Constants for the Avalon Nano 3S integration."""

DOMAIN = "avalon_nano3s"

# Config Keys
CONF_HOST = "host"
CONF_PORT = "port"
CONF_TIMEOUT = "timeout"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_WEB_PASSWORD = "web_password"

# Default values
DEFAULT_PORT = 4028
DEFAULT_TIMEOUT = 5
DEFAULT_UPDATE_INTERVAL = 10
DEFAULT_WEB_PASSWORD = "admin"
DEFAULT_WEB_USER = "admin"

# Fallback pools – zentral
FALLBACK_POOLS = {
    1: {"url": "stratum+tcp://pool1.com:3333", "user": "wallet.miner1", "pass": "x"},
    2: {"url": "stratum+tcp://pool2.com:3333", "user": "wallet.miner2", "pass": "x"},
    3: {"url": "stratum+tcp://pool3.com:3333", "user": "wallet.miner3", "pass": "x"},
}
