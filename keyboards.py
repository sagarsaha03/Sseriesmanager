# keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_admin_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="➕ Add Channel", callback_data="admin:add_channel")
    keyboard.button(text="📋 List Channels", callback_data="admin:list_channels")
    keyboard.button(text="🔁 Reload Config", callback_data="admin:reload")
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_duplicate_action_keyboard(original_msg_id: int, chat_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Keep Both",
                callback_data=f"dup:keep:{chat_id}:{original_msg_id}"
            ),
            InlineKeyboardButton(
                text="🗑️ Delete New",
                callback_data=f"dup:delete:{chat_id}:{original_msg_id}"
            )
        ]
    ])

def get_help_keyboard(pages: list[str], current_index: int):
    keyboard = InlineKeyboardBuilder()

    if current_index > 0:
        keyboard.button(text="⬅️ Prev", callback_data=f"help:page:{current_index-1}")
    keyboard.button(text=f"{current_index+1}/{len(pages)}", callback_data="help:noop")
    if current_index < len(pages) - 1:
        keyboard.button(text="➡️ Next", callback_data=f"help:page:{current_index+1}")

    keyboard.adjust(3)
    return keyboard.as_markup()
