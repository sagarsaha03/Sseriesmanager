# router_forwarder.py

from aiogram import Router, F
from aiogram.types import Message
from config import load_config
from classifier import classify_content
from utils import forward_message, log_action, is_admin, get_configured_channels

forward_router = Router()
config = load_config()

@forward_router.message(F.forward_date)
async def handle_forwarded_message(message: Message):
    channels = get_configured_channels()
    if not channels:
        await message.answer("❌ No channel mappings set. Use /set_channel to configure.")
        return

    try:
        content_type = classify_content(message)
        if content_type not in channels:
            await log_action(f"❗ Unknown content type: {content_type}")
            return

        targets = channels[content_type]
        await forward_message(message, targets['main'])
        await forward_message(message, targets['backup'])

        await log_action(
            f"✅ Forwarded to {content_type}\nMain: {targets['main']}\nBackup: {targets['backup']}"
        )

    except Exception as e:
        await log_action(f"❌ Error in forwarding: {e}")

@forward_router.message(F.text == "/reload")
async def reload_config_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    load_config(force_reload=True)
    await message.answer("🔄 Config reloaded.")
