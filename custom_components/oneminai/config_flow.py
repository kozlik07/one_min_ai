import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers import aiohttp_client

from .const import DOMAIN, API_BASE_URL

class OneMinAIFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            session = aiohttp_client.async_get_clientsession(self.hass)
            headers = {"API-KEY": api_key, "Content-Type": "application/json"}  # Zmienione!
            payload = {
                "type": "CHAT_WITH_AI",
                "model": "gpt-4o-mini",
                "promptObject": {"prompt": "hi"}  # Uproszczone do minimum
            }
            try:
                async with session.post(f"{API_BASE_URL}/features", headers=headers, json=payload) as resp:  # Zmieniony endpoint!
                    if resp.status == 200:
                        return self.async_create_entry(title="1min.AI", data=user_input)
                    elif resp.status == 401:
                        errors["base"] = "invalid_api_key"
                    else:
                        errors["base"] = f"api_error_{resp.status}"
                        self.hass.log(f"1min.ai test response: {resp.status} - {await resp.text()}")
            except Exception as err:
                errors["base"] = "cannot_connect"
                self.hass.log(f"1min.ai connection error: {err}")

        data_schema = vol.Schema({vol.Required(CONF_API_KEY): str})
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
