import json
from pathlib import Path

CONFIG_FILE = Path("config.json")

default_data = {
    "source_channels": [],
    "main_channels": {},
    "backup_channels": {},
    "delay": 3,
    "tmdb_key": ""
}

def load_config():
    if not CONFIG_FILE.exists():
        save_config(default_data)
    with CONFIG_FILE.open("r") as f:
        return json.load(f)

def save_config(data):
    with CONFIG_FILE.open("w") as f:
        json.dump(data, f, indent=4)

def add_channel(channel_type, key, value):
    data = load_config()
    if channel_type == "source":
        if value not in data["source_channels"]:
            data["source_channels"].append(value)
    elif channel_type == "main":
        data["main_channels"][key.lower()] = value
    elif channel_type == "backup":
        data["backup_channels"][key.lower()] = value
    save_config(data)

def set_delay(seconds):
    data = load_config()
    data["delay"] = int(seconds)
    save_config(data)

def set_tmdb_key(api_key):
    data = load_config()
    data["tmdb_key"] = api_key
    save_config(data)

def get_tmdb_key():
    return load_config().get("tmdb_key", "")

def get_delay():
    return load_config().get("delay", 3)

def get_channels():
    data = load_config()
    return data["source_channels"], data["main_channels"], data["backup_channels"]
