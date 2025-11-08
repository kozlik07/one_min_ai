import logging
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, API_BASE_URL, DEFAULT_MODEL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up 1min.AI from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_API_KEY: entry.data[CONF_API_KEY]
    }

    # Register the chat service
    async def chat_service(call):
        api_key = hass.data[DOMAIN][entry.entry_id][CONF_API_KEY]
        prompt = call.data.get("prompt", "Hello")
        model = call.data.get("model", DEFAULT_MODEL)
        web_search = call.data.get("web_search", True)
        num_of_site = call.data.get("num_of_site", 1)
        max_word = call.data.get("max_word", 500)

        session = async_get_clientsession(hass)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "type": "CHAT_WITH_AI",
            "model": model,
            "promptObject": {
                "prompt": prompt,
                "isMixed": False,
                "imageList": [],
                "webSearch": web_search,
                "numOfSite": num_of_site,
                "maxWord": max_word
            }
        }

        try:
            async with session.post(f"{API_BASE_URL}/chat", headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    _LOGGER.info(f"1min.AI response: {data}")
                    # Zakładam, że odpowiedź jest w polu 'response' – dostosuj na podstawie realnego API
                    hass.bus.async_fire("oneminai_response", {"response": data.get("response", "No response")})
                else:
                    _LOGGER.error(f"Error {response.status}: {await response.text()}")
        except Exception as err:
            _LOGGER.error(f"Error calling 1min.AI API: {err}")

    hass.services.async_register(DOMAIN, "chat", chat_service)

    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.services.async_remove(DOMAIN, "chat")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
