# utils.py

import json
import os
from config import CONFIG_FILE, ADMIN_ID
from aiogram.types import Message
from datetime import datetime
from aiogram import Bot

CONFIG_PATH = CONFIG_FILE if os.path.exists(CONFIG_FILE) else "config.json"

def is_admin(user_id: int) -> bool:
    return str(user_id) == str(ADMIN_ID)

def save_channel_mapping(category: str, main_id: str, backup_id: str):
    config = load_config_file()
    config.setdefault("channel_mappings", {})[category] = {
        "main": main_id,
        "backup": backup_id
    }
    save_config_file(config)

def get_configured_channels():
    config = load_config_file()
    return config.get("channel_mappings", {})

def load_config_file() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config_file(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

async def log_action(bot: Bot, log_channel_id: str, text: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        await bot.send_message(log_channel_id, f"🕒 {timestamp}\n{text}")
    except Exception as e:
        print(f"Logging failed: {e}")

async def forward_message(bot: Bot, from_chat_id: int, message: Message, to_chat_id: int):
    try:
        if message.text:
            await bot.send_message(to_chat_id, message.text)
        elif message.photo:
            await bot.send_photo(to_chat_id, message.photo[-1].file_id, caption=message.caption)
        elif message.video:
            await bot.send_video(to_chat_id, message.video.file_id, caption=message.caption)
        else:
            await bot.copy_message(to_chat_id, from_chat_id, message.message_id)
        return True
    except Exception as e:
        print(f"Forwarding failed: {e}")
        return False
