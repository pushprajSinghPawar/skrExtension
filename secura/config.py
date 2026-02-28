import os
import json

CONFIG_FILE = "config.json"

# default values stored when no config file exists
DEFAULTS = {
    "default_save_path": os.path.expanduser("~"),
    "default_image_path": os.path.expanduser("~"),
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        # ensure every key we expect is present
        for key, val in DEFAULTS.items():
            cfg.setdefault(key, val)
        return cfg
    # return a fresh copy so caller may mutate freely
    return DEFAULTS.copy()


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


# global configuration object used by UI
config = load_config()
