# config.py

import json
import os
from dataclasses import dataclass
from typing import Optional

CONFIG_FILE = "config.json"

@dataclass
class Config:
    bot_token: str
    admin_id: int
    tmdb_api_key: Optional[str] = None
    delay: float = 2.0
    channels: dict = None

def load_config() -> Config:
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError("❌ config.json file not found!")

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    return Config(
        bot_token=data.get("bot_token"),
        admin_id=data.get("admin_id"),
        tmdb_api_key=data.get("tmdb_api_key"),
        delay=data.get("delay", 2.0),
        channels=data.get("channels", {})
    )

def save_config(config: Config):
    data = {
        "bot_token": config.bot_token,
        "admin_id": config.admin_id,
        "tmdb_api_key": config.tmdb_api_key,
        "delay": config.delay,
        "channels": config.channels,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)
