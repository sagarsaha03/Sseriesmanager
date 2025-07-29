# config.py

import json
import os
from dataclasses import dataclass

CONFIG_FILE = "config.json"

@dataclass
class Config:
    bot_token: str
    admin_id: int
    tmdb_api_key: str = ""

def load_config() -> Config:
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found")

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    return Config(
        bot_token=data["bot_token"],
        admin_id=int(data["admin_id"]),
        tmdb_api_key=data.get("tmdb_api_key", "")
    )
