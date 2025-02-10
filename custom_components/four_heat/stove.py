from dataclasses import dataclass
from .tcp import TCPClient

def __convertSignedValue(value: int) -> int:
        """Convert a signed value to an integer."""
        print(f"{value =}")
        if value > 32767:
            value = (65536 - value) * -1
        return value


def test(command):
        """Read a single command response and return the parsed response."""
        print(f"\n\n {command}")
        command_type = int(command[:2], 16)
        print(f"{command_type =}")
        resp = {}

        if command_type == 1:  # th_all
            resp = {
                "command_type": "th_all",
                "command_code": command[:2],
                "id": int(command[2:4], 16),
                "parent": int(command[4:6], 16),
                "enablement": int(command[6:8], 16),
                "status": int(command[8:10], 16),
                "value": int(command[10:12], 16),
                "min": int(command[12:14], 16),
                "max": int(command[14:16], 16),
                "read_only": int(command[16:18], 16),
                "temperature": int(command[18:20], 16),
            }
        elif command_type == 2:  # th_temp
            resp = {
                "command_type": "th_temp",
                "command_code": command[:2],
                "id": int(command[2:4], 16),
                "parent": int(command[4:6], 16),
                "temperature": __convertSignedValue(int(command[6:10], 16)),
            }
        elif command_type == 3:  # th_state
            resp = {
                "command_type": "th_state",
                "command_code": command[:2],
                "id": int(command[2:4], 16),
                "parent": int(command[4:6], 16),
                "status": int(command[6:8], 16),
                "error_type": int(command[8:10], 16),
                "cod_error": int(command[10:12], 16),
            }
        elif command_type == 6:  # pw_all
            resp = {
                "command_type": "pw_all",
                "command_code": command[:2],
                "id": int(command[2:4], 16),
                "value": int(command[4:6], 16),
                "min": int(command[6:8], 16),
                "max": int(command[8:10], 16),
                "read_only": int(command[10:12], 16),
            }
        elif command_type == 8:  # crono_enb
            resp = {
                "command_type": "crono_enb",
                "command_code": command[:2],
                "id": int(command[2:4], 16),
                "status": int(command[4:6], 16),
                "mode": int(command[6:8], 16),
            }
        elif command_type == 11:  # stat_syst
            resp = {
                "command_type": "stat_syst",
                "command_code": command[:2],
                "id": int(command[2:4], 16),
                "status": int(command[4:6], 16),
                "var_status": int(command[6:8], 16),
            }
        elif command_type == 12:  # state_info
            if command[2:4] in ["00", "01", "80"]:
                str_value = "".join(
                    [
                        chr(int(command[i : i + 2], 16))
                        for i in range(4, len(command), 2)
                    ]
                )
                resp = {
                    "command_type": "state_info",
                    "command_code": command[:2],
                    "id": int(command[2:4], 16),
                    "stringa": str_value,
                }
            elif command[2:4] == "81":
                if len(command) == 28:
                    resp = {
                        "command_type": "state_info_81",
                        "command_code": command[:2],
                        "id": int(command[2:4], 16),
                        "status_crono": int(command[4:6], 16),
                        "liv_pot": chr(int(command[6:8], 16)),
                        "lang": int(command[8:10], 16),
                        "num_recipe": int(command[10:12], 16),
                        "ind_RS485": int(command[12:14], 16),
                        "thermostat": int(command[24:28], 16),
                    }
                else:
                    resp = {
                        "command_type": "state_info_81",
                        "command_code": command[:2],
                        "id": int(command[2:4], 16),
                        "status_crono": int(command[4:6], 16),
                        "liv_pot": chr(int(command[6:8], 16)),
                        "lang": int(command[8:10], 16),
                        "num_recipe": int(command[10:12], 16),
                        "ind_RS485": int(command[12:14], 16),
                        "thermostat": int(command[24:28], 16),
                        "pos_punto": int(command[28:30], 16),
                    }
        elif command_type == 14:  # par_value
            resp = {
                "command_type": "par_value",
                "command_code": command[:2],
                "id": int(command[2:6], 16),
                "value": __convertSignedValue(int(command[6:10], 16)),
                "min": __convertSignedValue(int(command[10:14], 16)),
                "max": __convertSignedValue(int(command[14:18], 16)),
                "read_only": int(command[18:20], 16),
                "pos_punto": int(command[20:22], 16),
                "step_incr": int(command[22:26], 16),
                "id_par": int(command[26:30], 16),
            }
            print(command[6:10], 16)
            print(hex(5))
            print(f"fuckkk {command[10:28]= }")
        elif command_type == 16:  # main_values
            if len(command) == 36:
                resp = {
                    "command_type": "main_values",
                    "command_code": command[:2],
                    "temp_sec": __convertSignedValue(int(command[6:10], 16)),
                    "status": int(command[10:12], 16),
                    "cod_error": int(command[12:14], 16),
                    "temp_princ": __convertSignedValue(int(command[20:24], 16)),
                }
            else:
                resp = {
                    "command_type": "main_values",
                    "command_code": command[:2],
                    "temp_sec": __convertSignedValue(int(command[6:10], 16)),
                    "status": int(command[10:12], 16),
                    "cod_error": int(command[12:14], 16),
                    "temp_princ": __convertSignedValue(int(command[20:24], 16)),
                    "pos_punto": int(command[36:38], 16),
                }
        elif command_type == 18:  # testout
            resp = {
                "command_type": "testout",
                "command_code": command[:2],
                "id": int(command[2:6], 16),
                "value": __convertSignedValue(int(command[6:10], 16)),
                "min": __convertSignedValue(int(command[10:14], 16)),
                "max": __convertSignedValue(int(command[14:18], 16)),
                "read_only": int(command[18:20], 16),
                "pos_punto": int(command[20:22], 16),
                "step_incr": int(command[22:26], 16),
                "test_timer": int(command[30:34], 16),
                "set_temperature_command": command[10:28],
            }
        elif command_type == 34:  # th_all_2
            resp = {
                "command_type": "th_all_2",
                "command_code": command[:2],
                "id": int(command[2:4], 16),
                "parent": int(command[4:6], 16),
                "enablement": int(command[6:8], 16),
                "status": int(command[8:10], 16),
                "value": __convertSignedValue(int(command[10:14], 16)),
                "min": __convertSignedValue(int(command[14:18], 16)),
                "max": __convertSignedValue(int(command[18:22], 16)),
                "temperature": __convertSignedValue(int(command[26:30], 16)),
                "pos_punto": int(command[30:32], 16),
            }
        print(resp)
        return resp

@dataclass
class UncompletedConfig:
    id: int
    value: int
    min_value: int
    max_value: int
    step: int
    command: str


class Stove:

    def __init__(self, client: TCPClient):
        
        self.client = client
        self.config: dict[int, UncompletedConfig] = {}
        self.thermostat: int | None = None 


    def _parse_config_data(self, data: str):
        data_type = int(data[:2], 16)
        if data_type == 12:
            if data[2:4] == '81':
                self.thermostat = int(data[24:28], 16)
        
        if data_type in [14, 18]:
            if not int(data[18:20], 16): # ignore read only data
                config_id = int(data[2:6], 16)
                self.config[config_id] = UncompletedConfig(
                    id=config_id,
                    value=int(data[6:10], 16),
                    min_value=int(data[10:14], 16),
                    max_value=int(data[14:18], 16),
                    step=int(data[22:26], 16),
                    command=data[10:28]
                )

            

    async def init_config(self):
        config = await self.client.read_config()
        # 006401900001000100
        for data in config[2:]:
            self._parse_config_data(data)
        print(self.thermostat)
        from pprint import pprint
        pprint(self.config)
