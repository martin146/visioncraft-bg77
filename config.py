import yaml
import os.path
from consts import *
from schema import Schema, SchemaError, And, Or
from logging import WARNING, INFO, DEBUG, ERROR

class ConfigService:

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.config = None

        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"Config file {config_path} not found")
        else:
            with open(config_path, "r") as f:
                self.config = yaml.load(f, Loader=yaml.SafeLoader)

    def validate_config(self) -> None:
        conf_schema = Schema({
            'Port': And(str, len),
            'BaudRate': And(int, lambda n: n > 0),
            'APN': And(str, len),
            'Band': [lambda s: s in BANDS.keys()],
            'Tech': lambda s: s in MODES.keys(),
            'RegTimeout': And(int, lambda n: n > 0),
            'CmdTimeout': And(int, lambda n: n > 0),
            'PLMN': Or(int, 'AUTO'),
            'Logging': {
                'file': And(str, len),
                'level': lambda s: s in ('debug', 'info', 'warning', 'error', 'critical'),
            }
        })

        try:
            conf_schema.validate(self.config)
        except SchemaError as e:
            raise e

    def get_log_level(self) -> int:
        level = self.config[LOG_SECTION][LOG_LEVEL]
        if level == 'info':
            return INFO
        elif level == 'warning':
            return WARNING
        elif level == 'debug':
            return DEBUG
        else:
            return ERROR