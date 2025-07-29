# utils.py
import json
from config import CONFIG_PATH, load_config
from aiogram.types import Message
from datetime import datetime

def is_admin(user_id: int) -> bool:
    config = load_config()
    return user_id == config.admin_id

def save_channel_mapping(category: str, main_id: str, backup_id: str):
    config = load_config()
    config.channels[category] = {"main": main_id, "backup": backup_id}
    with open(CONFIG_PATH, "r+") as f:
        data = json.load(f)
        data["channels"] = config.channels
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def get_configured_channels() -> dict:
    config = load_config()
    return config.channels or {}

def log_action(message: Message, target_chat_id: int, status: str):
    config = load_config()
    if not config.log_channel_id:
        return

    log_text = (
        f"<b>🔁 Forward Log</b>\n"
        f"📨 <b>Message ID:</b> <code>{message.message_id}</code>\n"
        f"📤 <b>Target Channel:</b> <code>{target_chat_id}</code>\n"
        f"📅 <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"✅ <b>Status:</b> {status}"
    )
    try:
        from main import bot
        return bot.send_message(chat_id=config.log_channel_id, text=log_text)
    except Exception as e:
        print("Logging error:", e)
