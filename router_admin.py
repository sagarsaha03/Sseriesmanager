# router_admin.py

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from config import ADMIN_ID, load_config, save_config
from keyboards import get_admin_keyboard

router = Router(name=__name__)

def is_admin(msg: Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("start"))
async def start_cmd(msg: Message):
    if is_admin(msg):
        await msg.answer("👋 Welcome to SSeriesManager Admin Panel!", reply_markup=get_admin_keyboard())

@router.message(Command("set_channel"))
async def set_channel_cmd(msg: Message):
    if not is_admin(msg): return

    if not msg.reply_to_message:
        return await msg.reply("❗Please reply to a message from the channel to set it.")

    channel_id = msg.reply_to_message.forward_from_chat.id if msg.reply_to_message.forward_from_chat else None
    if not channel_id:
        return await msg.reply("⚠️ Unable to detect channel ID. Please forward a post from the channel and reply to that.")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Set as Source", callback_data=f"set_source:{channel_id}")],
        [InlineKeyboardButton(text="Set as Main Target", callback_data=f"set_target:{channel_id}")],
        [InlineKeyboardButton(text="Set as Backup", callback_data=f"set_backup:{channel_id}")]
    ])
    await msg.reply(f"🛠 What role should this channel have?\nChannel ID: `{channel_id}`", reply_markup=keyboard)

@router.callback_query(F.data.startswith("set_"))
async def handle_set_channel_callback(callback: CallbackQuery):
    role, channel_id = callback.data.split(":")
    config = load_config()

    if role == "set_source":
        config["channels"][channel_id] = {
            "category": None,
            "targets": [],
            "backups": []
        }
        await callback.message.edit_text(f"✅ Set as Source Channel: `{channel_id}`")
    elif role == "set_target":
        # You must first add as source
        found = False
        for src_id, val in config["channels"].items():
            if channel_id in val["targets"]:
                found = True
                break
        if not found:
            for src_id in config["channels"]:
                config["channels"][src_id]["targets"].append(channel_id)
                found = True
                break
        await callback.message.edit_text(f"✅ Set as Main Target Channel: `{channel_id}`")
    elif role == "set_backup":
        found = False
        for src_id in config["channels"]:
            config["channels"][src_id]["backups"].append(channel_id)
            found = True
            break
        await callback.message.edit_text(f"✅ Set as Backup Channel: `{channel_id}`")

    save_config(config)

@router.message(Command("list_channels"))
async def list_channels_cmd(msg: Message):
    if not is_admin(msg): return

    config = load_config()
    text = "**📋 Configured Channels:**\n\n"
    for src, info in config["channels"].items():
        text += f"🔹 Source: `{src}`\n"
        text += f"   ├ Category: `{info.get('category')}`\n"
        text += f"   ├ Targets: {', '.join([f'`{x}`' for x in info.get('targets', [])]) or 'None'}\n"
        text += f"   └ Backups: {', '.join([f'`{x}`' for x in info.get('backups', [])]) or 'None'}\n\n"

    await msg.reply(text or "⚠️ No channels configured.")
