# keyboards.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_help_keyboard(page: int = 0):
    pages = [
        [
            ("🔧 Settings Commands", "page:1"),
            ("📊 Channel Commands", "page:2"),
        ],
        [
            ("🧠 TMDB Commands", "page:3"),
            ("🆘 Bot Commands", "page:4"),
        ]
    ]

    keyboard = [
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1]) for btn in pages[page]]
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"nav:{page - 1}"))
    if page < len(pages) - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"nav:{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def back_to_help_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🔙 Back to Help", callback_data="help:main")]
    ])
