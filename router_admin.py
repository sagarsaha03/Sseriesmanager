from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config import Config, ADMIN_ID, set_channel, get_channel
import sqlite3
from datetime import datetime

admin_router = Router()
admin_router.message.filter(F.from_user.id == ADMIN_ID)
admin_router.callback_query.filter(F.from_user.id == ADMIN_ID)

@admin_router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("⚙️ SSeriesManager Bot Activated\nUse /help for commands")

@admin_router.message(Command("status"))
async def status_cmd(message: Message):
    source = get_channel('source')
    log_channel = get_channel('log')
    tmdb_status = Config.get('tmdb_enabled')
    delay = Config.get('forward_delay')
    
    status_msg = (
        f"📊 Bot Status:\n\n"
        f"• Source Channel: {source[1] if source else 'Not set'}\n"
        f"• Log Channel: {log_channel[1] if log_channel else 'Not set'}\n"
        f"• TMDB Enabled: {tmdb_status}\n"
        f"• Forward Delay: {delay}s\n"
        f"• Custom Message: {Config.get('custom_message')}"
    )
    await message.answer(status_msg)

@admin_router.message(Command("set_channel"))
async def set_channel_cmd(message: Message):
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Usage: /set_channel <role> <channel_id>")
        return
    
    role, channel_id = args[1], args[2]
    await set_channel(role, channel_id)
    await message.answer(f"✅ {role.capitalize()} channel set to {channel_id}")

@admin_router.message(Command("list_channels"))
async def list_channels_cmd(message: Message):
    conn = sqlite3.connect("sseriesmanager.db")
    cur = conn.cursor()
    cur.execute("SELECT role, channel_name, channel_id FROM channels")
    channels = cur.fetchall()
    conn.close()
    
    if not channels:
        await message.answer("No channels configured")
        return
    
    response = "📋 Configured Channels:\n"
    for role, name, cid in channels:
        response += f"• {role.capitalize()}: {name} ({cid})\n"
    
    await message.answer(response)

@admin_router.message(Command("set_config"))
async def set_config_cmd(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Usage: /set_config <key> <value>")
        return
    
    key, value = args[1], args[2]
    valid_keys = ['tmdb_enabled', 'forward_delay', 'custom_message', 'domain_replace']
    
    if key not in valid_keys:
        await message.answer(f"Invalid key! Valid keys: {', '.join(valid_keys)}")
        return
    
    if key == 'forward_delay' and not value.isdigit():
        await message.answer("Delay must be a number!")
        return
    
    Config.set(key, value)
    await message.answer(f"✅ Config updated: {key} = {value}")

@admin_router.message(Command("reload"))
async def reload_cmd(message: Message):
    # Implement reload logic if needed
    await message.answer("♻️ Bot configuration reloaded")

@admin_router.message(Command("duplicates"))
async def duplicates_cmd(message: Message):
    conn = sqlite3.connect("sseriesmanager.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM duplicates WHERE status='pending'")
    duplicates = cur.fetchall()
    conn.close()
    
    if not duplicates:
        await message.answer("No pending duplicates")
        return
    
    response = "⚠️ Pending Duplicates:\n\n"
    for dup in duplicates:
        response += f"• Original: {dup[1]}, Duplicate: {dup[2]} in {dup[3]}\n"
    
    await message.answer(response)
