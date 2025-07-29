# router_admin.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import Config, load_config
from utils import is_admin, save_channel_mapping, get_configured_channels
from keyboards import get_admin_keyboard

admin_router = Router()
config: Config = load_config()

@admin_router.message(CommandStart())
async def start_handler(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("👋 Welcome to SSeriesManager Bot!", reply_markup=get_admin_keyboard())

@admin_router.message(Command("set_channel"))
async def set_channel_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split()
    if len(args) != 4:
        await message.answer("❗ Usage:\n/set_channel <category> <main_channel_id> <backup_channel_id>")
        return

    _, category, main_id, backup_id = args
    save_channel_mapping(category.lower(), main_id, backup_id)
    await message.answer(f"✅ Channel mapping set for '{category}'")

@admin_router.message(Command("list_channels"))
async def list_channels_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    mappings = get_configured_channels()
    if not mappings:
        await message.answer("⚠️ No channels configured.")
        return

    text = "<b>📡 Configured Channels:</b>\n"
    for cat, ids in mappings.items():
        text += f"\n<b>{cat.title()}</b>\n➡️ Main: <code>{ids['main']}</code>\n🔁 Backup: <code>{ids['backup']}</code>\n"
    await message.answer(text)
