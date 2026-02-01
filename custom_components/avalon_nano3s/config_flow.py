# custom_components/avalon_nano3s/config_flow.py
import logging
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig
from .avalon_api import AsyncAvalonAPI
from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_TIMEOUT,
    CONF_UPDATE_INTERVAL,
    CONF_WEB_PASSWORD,
    FALLBACK_POOLS,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_WEB_PASSWORD,
)
_LOGGER = logging.getLogger(__name__)

# Schema für die Erstkonfiguration – Web-Passwort direkt nach Host als 2. Feld
BASE_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_WEB_PASSWORD, default=DEFAULT_WEB_PASSWORD): str,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): cv.positive_int,
})

class AvalonNano3SConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Basis-Konfiguration für Avalon Nano 3S"""
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors = {}

        if user_input is not None:
            # Validierung Web-Passwort
            web_pw = user_input.get(CONF_WEB_PASSWORD, "admin").strip()
            if not web_pw:
                errors[CONF_WEB_PASSWORD] = "empty_password"

            # Validierung Intervall
            interval = user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
            if not 1 <= interval <= 60:
                errors[CONF_UPDATE_INTERVAL] = "invalid_interval"
            
            if not errors:
                await self.async_set_unique_id(user_input[CONF_HOST].replace(".", "_"))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=BASE_SCHEMA,
            errors=errors
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return AvalonNano3SOptionsFlowHandler(config_entry)


class AvalonNano3SOptionsFlowHandler(config_entries.OptionsFlow):
    """Options-Flow mit allen Funktionen: Intervall, Web-Passwort, Pools"""
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry
        self._api = AsyncAvalonAPI(
            host=config_entry.data[CONF_HOST],
            port=config_entry.data[CONF_PORT],
            timeout=config_entry.data[CONF_TIMEOUT],
            web_password=config_entry.options.get(
                CONF_WEB_PASSWORD,
                config_entry.data.get(CONF_WEB_PASSWORD, "admin")
            ),
        )
        self._pool_index = None

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Startseite: Auswahl, was geändert werden soll"""
        if user_input is not None:
            action = user_input.get("action")
            if action == "interval":
                return await self.async_step_interval()
            if action == "web_password":
                return await self.async_step_web_password()
            if action in ("pool1", "pool2", "pool3"):
                self._pool_index = int(action[-1])
                return await self.async_step_pool()

        schema = vol.Schema({
            vol.Required("action"): SelectSelector(
                SelectSelectorConfig(
                    options=[
                        "interval",
                        "web_password",          # ← Zweite Position nach Intervall
                        "pool1",
                        "pool2",
                        "pool3",
                    ],
                    translation_key="action_selector"
                )
            )
        })

        return self.async_show_form(step_id="init", data_schema=schema)

    async def async_step_interval(self, user_input=None) -> FlowResult:
        """Update-Intervall ändern"""
        errors = {}
        current = str(self._config_entry.options.get(
            CONF_UPDATE_INTERVAL,
            self._config_entry.data.get(CONF_UPDATE_INTERVAL, 10)
        ))

        if user_input is not None:
            try:
                interval = int(user_input.get(CONF_UPDATE_INTERVAL, current))
                if 1 <= interval <= 60:
                    return self.async_create_entry(title="", data={CONF_UPDATE_INTERVAL: interval})
                errors[CONF_UPDATE_INTERVAL] = "invalid_interval"
            except ValueError:
                errors[CONF_UPDATE_INTERVAL] = "invalid_number"

        schema = vol.Schema({
            vol.Required(CONF_UPDATE_INTERVAL, default=current): str
        })

        return self.async_show_form(step_id="interval", data_schema=schema, errors=errors)

    async def async_step_web_password(self, user_input=None) -> FlowResult:
        """Web-Passwort ändern (nicht Pool-Passwörter!)"""
        errors = {}
        current_pw = self._config_entry.options.get(
            CONF_WEB_PASSWORD,
            self._config_entry.data.get(CONF_WEB_PASSWORD, "admin")
        )

        if user_input is not None:
            new_pw = user_input.get(CONF_WEB_PASSWORD, "").strip()
            if not new_pw:
                errors["base"] = "empty_password"
            else:
                # Options speichern + Integration sofort neu laden
                new_options = dict(self._config_entry.options)
                new_options[CONF_WEB_PASSWORD] = new_pw
                self.hass.config_entries.async_schedule_reload(self._config_entry.entry_id)
                return self.async_create_entry(title="", data=new_options)

        schema = vol.Schema({
            vol.Required(CONF_WEB_PASSWORD, default=current_pw): str
        })

        return self.async_show_form(
            step_id="web_password",
            data_schema=schema,
            errors=errors
        )

    async def async_step_pool(self, user_input=None) -> FlowResult:
        """Pool konfigurieren (HA-konform, sprachunabhängig)"""
        errors = {}
        idx = self._pool_index
    
        try:
            pools = await self._api.pools()
            pool = pools.get(f"p{idx}", {})
        except Exception as e:
            _LOGGER.debug("Pool API read failed: %s", e)
            pool = {}
        
        current_url = pool.get("URL") or self._config_entry.options.get(f"pool{idx}_url") or FALLBACK_POOLS[idx]["url"]
        current_user = pool.get("User") or self._config_entry.options.get(f"pool{idx}_user") or FALLBACK_POOLS[idx]["user"]
        current_pass = pool.get("Password") or self._config_entry.options.get(f"pool{idx}_password") or FALLBACK_POOLS[idx]["pass"]


    
        if user_input is not None:
            url = user_input.get("url", "").strip()
            user = user_input.get("user", "").strip()
            password = user_input.get("password", "").strip()
            if not (url and user and password):
                errors["base"] = "incomplete_pool"
            else:
                # Pool direkt über API setzen
                result = await self._api.set_pool(idx, url, user, password)
                if result.get("success"):
                    # Optionen speichern, damit die Flow-Werte konsistent bleiben
                    new_options = dict(self._config_entry.options)
                    new_options[f"pool{idx}_url"] = url
                    new_options[f"pool{idx}_user"] = user
                    new_options[f"pool{idx}_password"] = password
                    self.hass.config_entries.async_update_entry(self._config_entry, options=new_options)
    
                    # Reboot optional
                    reboot_result = await self._api.reboot()
                    if reboot_result.get("success"):
                        return self.async_abort(
                            reason="success",
                            description_placeholders={"pool_num": str(idx)}
                        )
                    errors["base"] = "reboot_failed"
                else:
                    errors["base"] = "unknown"
    
        schema = vol.Schema({
            vol.Required("url", default=current_url): str,
            vol.Required("user", default=current_user): str,
            vol.Required("password", default=current_pass): str,
        })
        
        return self.async_show_form(
            step_id="pool",
            data_schema=schema,
            errors=errors,
            description_placeholders={"pool_num": str(idx)}
        )