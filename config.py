import toml

from pathlib import Path


# TODO: set some scheme to TOML config or let argparse validate the dict
def load_config(config_path):
    parsed_toml = toml.load(config_path)
    return parsed_toml


def parse_config(config):
    if "input" in config and type(config["input"]) == str:
        config["input"] = Path(config["input"])
    if "output" in config and type(config["output"]) == str:
        config["output"] = Path(config["output"])

    return config
