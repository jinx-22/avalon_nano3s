import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_PASSWORD, CONF_NAME
from .api import AvalonNano3SAPI

class AvalonNano3SConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            password = user_input[CONF_PASSWORD]
            api = AvalonNano3SAPI(host, password)
            if api.login():
                return self.async_create_entry(
                    title=f"Avalon Nano 3S ({host})",
                    data=user_input
                )
            else:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Optional(CONF_NAME, default="Avalon Nano 3S"): str
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)