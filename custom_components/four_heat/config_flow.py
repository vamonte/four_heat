import logging
import voluptuous as vol
from homeassistant.data_entry_flow import FlowResult
from homeassistant import config_entries
from .const import DOMAIN
from .tcp import TCPClient
from .stove import Stove
_LOGGER = logging.getLogger(__name__)

class FourHeatLocalConfiGFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1

    # name "async_step_user" is mandatory
    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        _LOGGER.error(10)
        user_form = vol.Schema({
            vol.Required("ip"): str,
            vol.Required("port", default="8080"): str,
        })

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=user_form)
        
        _LOGGER.error(f"{user_input =}")
        tcp_client = TCPClient(user_input["ip"], user_input["port"])
        _LOGGER.error(0)
        stove = Stove(tcp_client)
        _LOGGER.error(1)
        await stove.init_config()
        _LOGGER.error(2)
        self._user_inputs.update({"toto": "aa"})

    async def step_complete_config(self, user_input: dict | None = None) -> FlowResult:
        print(self._user_inputs)