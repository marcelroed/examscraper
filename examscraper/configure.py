from sys import argv
from pathlib import Path
import pandas as pd

def read_configuration():
    config_path = _get_path(argv)
    config = _load_config(config_path)
    return config


def _get_path(arguments):
    # Validate argument length
    if not len(arguments) == 2:
        if len(arguments) > 2:
            raise ValueError("Too many arguments")
        raise ValueError("Too few arguments. Did you forget the config file?")
    filename = arguments[1]
    # Validate filetype
    if not filename[-5:] == ".json":
        raise ValueError("Wrong filetype, must be .json: " + filename)
    config = Path(filename)
    # Validate file existance
    if not config.is_file():
        raise ValueError("No such file: " + filename)
    return config

def _load_config(cfg_path):
    return pd.read_json(cfg_path.as_uri())
