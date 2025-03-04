import logging
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .api import OneMinAIAPI

_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register("one_min_ai")
class OneMinAIConfigFlow(config_entries.ConfigFlow, domain="one_min_ai"):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            api = OneMinAIAPI(user_input["api_key"])
            try:
                _LOGGER.debug(f"Attempting to fetch agents with API key: {user_input['api_key']}")
                agents = api.get_agents()
                if agents:
                    _LOGGER.debug(f"Successfully fetched agents: {agents}")
                    return self.async_create_entry(title="1min AI", data=user_input)
                else:
                    _LOGGER.error("No agents available")
                    errors["base"] = "no_agents_available"
            except Exception as e:
                _LOGGER.error(f"Error fetching agents: {str(e)}")
                errors["base"] = "invalid_api_key"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("api_key"): str,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OneMinAIOptionsFlowHandler(config_entry)

class OneMinAIOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        api = OneMinAIAPI(self.config_entry.data["api_key"])
        try:
            _LOGGER.debug(f"Attempting to fetch agents with API key: {self.config_entry.data['api_key']}")
            agents = api.get_agents()
            agent_choices = {agent["id"]: agent["name"] for agent in agents}
            _LOGGER.debug(f"Successfully fetched agents: {agent_choices}")
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Required("agent_id", default=self.config_entry.options.get("agent_id", "")): vol.In(agent_choices),
                }),
            )
        except Exception as e:
            _LOGGER.error(f"Error fetching agents: {str(e)}")
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Required("agent_id", default=self.config_entry.options.get("agent_id", "")): str,
                }),
                errors={"base": "invalid_api_key"},
            )

