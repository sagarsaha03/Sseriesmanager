# utils.py

import json
import os
from datetime import datetime
from aiogram.types import Message

CONFIG_FILE = "channel_mappings.json"
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")  # Optional: for logging

# --- ADMIN CHECK ---
def is_admin(user_id: int) -> bool:
    return str(user_id) == os.getenv("ADMIN_ID")

# --- CHANNEL CONFIG MANAGEMENT ---
def save_channel_mapping(category: str, main_channel: str, backup_channel: str):
    mappings = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            mappings = json.load(f)

    mappings[category] = {
        "main": main_channel,
        "backup": backup_channel
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(mappings, f, indent=4)

def get_configured_channels():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# --- FORWARDING FUNCTION ---
async def forward_message(bot, message: Message, target_chat_id: int):
    if message.photo:
        await bot.send_photo(
            chat_id=target_chat_id,
            photo=message.photo[-1].file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )
    elif message.video:
        await bot.send_video(
            chat_id=target_chat_id,
            video=message.video.file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )
    elif message.document:
        await bot.send_document(
            chat_id=target_chat_id,
            document=message.document.file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )
    elif message.text:
        await bot.send_message(
            chat_id=target_chat_id,
            text=message.text,
            parse_mode="HTML"
        )

# --- LOGGING FUNCTION ---
async def log_action(bot, status: str, category: str, to_channel: str, message_id: int):
    if not LOG_CHANNEL_ID:
        return

    log_text = (
        f"✅ <b>Forward Status:</b> {status}\n"
        f"📁 <b>Category:</b> {category}\n"
        f"📤 <b>To Channel:</b> <code>{to_channel}</code>\n"
        f"🕒 <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🔗 <b>Message ID:</b> <code>{message_id}</code>"
    )

    await bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text, parse_mode="HTML")
