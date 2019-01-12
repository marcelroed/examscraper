import codecs
import json
from pathlib import Path


def read_configuration(argv):
    config_path = _get_path(argv)
    config = _load_config(config_path)
    return config


def _get_path(arguments):
    # Validate argument length
    if not len(arguments) == 1:
        if len(arguments) > 1:
            raise ValueError("Too many arguments:", arguments)
        raise ValueError("Too few arguments. Did you forget the config file?")
    filename = arguments[0]
    # Validate filetype
    if not filename[-5:] == ".json":
        raise ValueError("Wrong filetype, must be .json: " + filename)
    config = Path(filename)
    # Validate file existence
    if not config.is_file():
        raise ValueError("No such file: " + filename)
    return config


def _load_config(cfg_path):
    with codecs.open(cfg_path, 'r', encoding='UTF-8') as f:
        return json.load(f)
