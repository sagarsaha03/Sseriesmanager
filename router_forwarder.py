# router_forwarder.py

from aiogram import Router, types
from aiogram.types import Message
from config import load_config, ADMIN_ID
from classifier import classify_title
from utils import modify_text_and_caption, is_duplicate, mark_as_forwarded
from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError

router = Router(name=__name__)

@router.message()
async def forward_handler(msg: Message):
    if not msg.chat or not msg.chat.id:
        return

    config = load_config()
    src_id = str(msg.chat.id)

    if src_id not in config["channels"]:
        return  # Skip unknown source

    category = config["channels"][src_id].get("category")
    if not category:
        # Auto classify using title
        title = msg.text or msg.caption or ""
        category = classify_title(title)

    target_ids = config["channels"][src_id].get("targets", [])
    backup_ids = config["channels"][src_id].get("backups", [])

    if not target_ids:
        await msg.bot.send_message(ADMIN_ID, f"⚠️ No target channel set for source `{src_id}`.")
        return

    title = msg.text or msg.caption or ""

    if is_duplicate(title, src_id):
        duplicate_link = f"https://t.me/c/{str(src_id)[4:]}/{msg.message_id}"
        await msg.bot.send_message(
            ADMIN_ID,
            f"⚠️ Duplicate detected in same channel:\n🔗 [View Message]({duplicate_link})\n\nTitle:\n`{title}`",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    new_text, new_caption = modify_text_and_caption(msg)

    success_count = 0
    fail_count = 0

    for channel_id in target_ids + backup_ids:
        try:
            if msg.text:
                await msg.bot.send_message(channel_id, new_text or msg.text)
            elif msg.photo:
                await msg.bot.send_photo(channel_id, photo=msg.photo[-1].file_id, caption=new_caption or msg.caption)
            elif msg.document:
                await msg.bot.send_document(channel_id, document=msg.document.file_id, caption=new_caption or msg.caption)
            else:
                continue
            success_count += 1
        except (TelegramForbiddenError, TelegramAPIError) as e:
            await msg.bot.send_message(ADMIN_ID, f"❌ Failed to forward to `{channel_id}`:\n`{e}`")
            fail_count += 1

    mark_as_forwarded(title, src_id)

    await msg.bot.send_message(
        ADMIN_ID,
        f"✅ Forward Report:\n• Source: `{src_id}`\n• Category: `{category}`\n• Title: `{title[:60]}...`\n• ✅ Success: {success_count} | ❌ Failed: {fail_count}"
    )
