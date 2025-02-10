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
    _user_inputs: dict = {}

    # name "async_step_user" is mandatory
    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        _LOGGER.error(10)
        user_form = vol.Schema({
            vol.Required("ip"): str,
            vol.Required("port", default="80"): str,
        })

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=user_form)
        
        self._user_inputs.update(user_input)
        tcp_client = TCPClient(user_input["ip"], user_input["port"])
        stove = Stove(tcp_client)
        await stove.init_config()
        self._user_inputs.update({"config": stove.config})
        await self.step_complete_config()

    async def step_complete_config(self, user_input: dict | None = None) -> FlowResult:
        
        fields = {}
        for i, config in enumerate(self._user_inputs["config"].items()):
            fields[vol.Required(f"config_{i}")] = str