# router_forwarder.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Message
from config import load_config
from utils import (
    is_admin,
    forward_message,
    classify_message,
    get_channel_ids_by_category,
    log_action,
    update_forward_status
)

forwarder_router = Router()
config = load_config()

@forwarder_router.message()
async def handle_forward(message: Message):
    # Skip messages from self or system messages
    if message.chat.type != "channel":
        return

    # Only process messages from the configured source channel
    if str(message.chat.id) != str(config.source_channel_id):
        return

    # Classify the message into category
    category = classify_message(message)
    if not category:
        await log_action(message, "❌ Unclassified", "unknown", None)
        return

    # Get target channels
    targets = get_channel_ids_by_category(category)
    if not targets:
        await log_action(message, f"❌ No target for '{category}'", category, None)
        return

    # Forward to main and backup
    for target_type in ["main", "backup"]:
        try:
            channel_id = targets.get(target_type)
            if not channel_id:
                continue
            await forward_message(message, channel_id)
            await log_action(message, f"✅ Forwarded to {target_type}", category, channel_id)
        except Exception as e:
            await log_action(message, f"⚠️ Failed to forward to {target_type}: {e}", category, channel_id)

    await update_forward_status(message.message_id)
