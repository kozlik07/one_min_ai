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
