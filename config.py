# config.py

import json
from pathlib import Path

CONFIG_PATH = Path("data/config.json")

# Your bot token and admin ID
BOT_TOKEN = "8016591770:AAFXBKlZS0HRlm1ThGhOKXmNymAHHvnNTDE"
ADMIN_ID = 1588777572

# Load config from file
def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "channels": {},     # source_id: {category, targets, backups}
            "tmdb_enabled": False,
            "tmdb_key": "",
            "delay": 3
        }

# Save config to file
def save_config(data):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
