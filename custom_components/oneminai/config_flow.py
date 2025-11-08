import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers import aiohttp_client

from .const import DOMAIN, API_BASE_URL

class OneMinAIFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for 1min.AI."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            # Test API key z prostym chat request
            session = aiohttp_client.async_get_clientsession(self.hass)
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "type": "CHAT_WITH_AI",
                "model": "gpt-4o-mini",
                "promptObject": {
                    "prompt": "hi",
                    "isMixed": False,
                    "imageList": [],
                    "webSearch": False,
                    "numOfSite": 1,
                    "maxWord": 100
                }
            }
            try:
                async with session.post(f"{API_BASE_URL}/chat", headers=headers, json=payload) as response:
                    if response.status == 200:
                        # Sukces! Key valid
                        return self.async_create_entry(title="1min.AI", data=user_input)
                    elif response.status == 401:
                        errors["base"] = "invalid_api_key"
                    else:
                        errors["base"] = "cannot_connect"
                        # Loguj dla debugu
                        self.hass.log(f"1min.ai test response: {response.status} - {await response.text()}")
            except Exception as err:
                errors["base"] = "cannot_connect"
                self.hass.log(f"1min.ai connection error: {err}")

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
