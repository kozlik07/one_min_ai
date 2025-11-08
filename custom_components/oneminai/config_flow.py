import voluptuous as vol

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
            # Test API key
            session = aiohttp_client.async_get_clientsession(self.hass)
            headers = {"Authorization": f"Bearer {api_key}"}
            try:
                async with session.get(f"{API_BASE_URL}/health", headers=headers) as response:  # Zakładam endpoint /health do testu
                    if response.status == 200:
                        return self.async_create_entry(title="1min.AI", data=user_input)
                    else:
                        errors["base"] = "invalid_api_key"
            except Exception:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
