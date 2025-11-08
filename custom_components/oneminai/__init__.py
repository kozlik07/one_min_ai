
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
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {CONF_API_KEY: entry.data[CONF_API_KEY]}

    async def chat_service(call):
        api_key = hass.data[DOMAIN][entry.entry_id][CONF_API_KEY]
        prompt = call.data.get("prompt", "Hello")
        model = call.data.get("model", DEFAULT_MODEL)
        web_search = call.data.get("web_search", False)  # Opcjonalne, default False
        num_of_site = call.data.get("num_of_site", 1)
        max_word = call.data.get("max_word", 500)

        session = async_get_clientsession(hass)
        headers = {"API-KEY": api_key, "Content-Type": "application/json"}  # Zmienione!
        payload = {
            "type": "CHAT_WITH_AI",
            "model": model,
            "promptObject": {"prompt": prompt}
        }
        # Dodaj opcjonalne pola jeśli potrzebne (testuj!)
        if web_search:
            payload["promptObject"].update({
                "webSearch": web_search,
                "numOfSite": num_of_site,
                "maxWord": max_word
            })

        try:
            async with session.post(f"{API_BASE_URL}/features", headers=headers, json=payload) as response:  # Zmieniony endpoint!
                if response.status == 200:
                    data = await response.json()
                    _LOGGER.info(f"1min.AI response: {data}")
                    hass.bus.async_fire("oneminai_response", {"response": data.get("response", "No response")})
                else:
                    error_text = await response.text()
                    _LOGGER.error(f"1min.AI API error {response.status}: {error_text}")
                    hass.bus.async_fire("oneminai_error", {"error": error_text})
        except Exception as err:
            _LOGGER.error(f"Error calling 1min.AI API: {err}")

    hass.services.async_register(DOMAIN, "chat", chat_service)
    return True

async def async_unload_entry(hass, entry):
    hass.services.async_remove(DOMAIN, "chat")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
