import requests
import logging

_LOGGER = logging.getLogger(__name__)

class AvalonNano3SAPI:
    def __init__(self, host, password):
        self.host = host
        self.password = password
        self.session = requests.Session()
        self.auth = None

    def login(self):
        try:
            url = f"http://{self.host}/get_auth.cgi"
            r = self.session.get(url)
            data = r.json()
            self.auth = data.get("auth")
            self.session.cookies.set("auth", self.auth)
            return True
        except Exception as e:
            _LOGGER.error("Login failed: %s", e)
            return False

    def get_dashboard(self):
        url = f"http://{self.host}/get_dashboard.cgi"
        r = self.session.get(url, params={"num": "0.123456"})
        data = r.json()
        return data

    def set_power_mode(self, mode):
        url = f"http://{self.host}/set_power.cgi"
        r = self.session.post(url, data={"mode": mode})
        return r.status_code == 200