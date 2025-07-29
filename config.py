# config.py

from pathlib import Path
import json
import os

# Bot credentials
BOT_TOKEN = "8016591770:AAFXBKlZS0HRlm1ThGhOKXmNymAHHvnNTDE"
ADMIN_ID = 1588777572  # Your Telegram user ID

# TMDB API (optional - can be set via command)
TMDB_API_KEY = ""

# Delay between forwards (can be changed via bot command)
FORWARD_DELAY = 3  # in seconds

# Path to JSON database file
DB_FILE = "channels.json"


# --- Helper functions to load and save config ---

def load_config():
    if not Path(DB_FILE).exists():
        return {
            "source_channels": [],
            "target_channels": {},
            "backup_channels": {},
            "categories": {},
            "tmdb_enabled": False,
            "tmdb_api_key": TMDB_API_KEY,
            "forward_delay": FORWARD_DELAY
        }
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# --- Create file if not present ---
if not os.path.exists(DB_FILE):
    save_config(load_config())
