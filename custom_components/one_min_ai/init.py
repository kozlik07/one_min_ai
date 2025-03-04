from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv

DOMAIN = "one_min_ai"

async def async_setup(hass, config):
    """Set up the 1min AI component."""
    hass.data[DOMAIN] = {}
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform("sensor", DOMAIN, {}, config)
    )
    return True

async def async_setup_entry(hass, config_entry):
    """Set up 1min AI from a config entry."""
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True

