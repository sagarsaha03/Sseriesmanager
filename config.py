# config.py
import json
from dataclasses import dataclass
from pathlib import Path

CONFIG_PATH = Path("config.json")

@dataclass
class Config:
    bot_token: str
    admin_id: int
    tmdb_api_key: str = ""
    channels: dict = None
    delay: float = 1.5
    log_channel_id: str = ""

def load_config() -> Config:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        return Config(
            bot_token=data["bot_token"],
            admin_id=int(data["admin_id"]),
            tmdb_api_key=data.get("tmdb_api_key", ""),
            channels=data.get("channels", {}),
            delay=data.get("delay", 1.5),
            log_channel_id=data.get("log_channel_id", "")
        )
    else:
        default = {
            "bot_token": "YOUR_BOT_TOKEN",
            "admin_id": 123456789,
            "tmdb_api_key": "",
            "channels": {},
            "delay": 1.5,
            "log_channel_id": ""
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(default, f, indent=4)
        raise Exception("⚠️ config.json created. Fill it and restart.")
