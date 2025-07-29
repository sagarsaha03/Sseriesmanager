# keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Set Channel", callback_data="set_channel")],
        [InlineKeyboardButton(text="📋 List Channels", callback_data="list_channels")],
        [InlineKeyboardButton(text="⚙️ Reload", callback_data="reload")],
        [InlineKeyboardButton(text="🛰️ Status", callback_data="status")],
    ])
    return keyboard
