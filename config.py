# config.py

from typing import Optional
from pydantic import BaseModel
import json
import os

CONFIG_FILE = "config.json"

class ChannelConfig(BaseModel):
    source_channel: Optional[int] = None
    main_target: Optional[int] = None
    backup_target: Optional[int] = None

class BotConfig(BaseModel):
    bot_token: str
    admin_id: int
    tmdb_api_key: Optional[str] = None
    delay: float = 3.0
    channels: dict[str, ChannelConfig] = {}

def load_config() -> BotConfig:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return BotConfig(**data)
    else:
        raise FileNotFoundError("Config file not found")

def save_config(config: BotConfig):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config.dict(), f, indent=2)
