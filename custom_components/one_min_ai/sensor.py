from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv

from . import DOMAIN
from .api import OneMinAIAPI

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the 1min AI sensor from a config entry."""
    api_key = config_entry.data["api_key"]
    agent_id = config_entry.options.get("agent_id", "")
    
    api = OneMinAIAPI(api_key)
    
    async_add_entities([OneMinAISensor(hass, api, agent_id)], True)

class OneMinAISensor(Entity):
    def __init__(self, hass, api, agent_id):
        self.hass = hass
        self._api = api
        self._agent_id = agent_id
        self._state = None

    @property
    def name(self):
        return "1min AI Sensor"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            response = self._api.generate_text(self._agent_id, "Hello, what's the weather like today?")
            self._state = response.get("text", "Error fetching data")
        except Exception as e:
            self._state = f"Error: {str(e)}"
