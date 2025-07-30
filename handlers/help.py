# handlers/help.py

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from keyboards import get_help_keyboard

router = Router(name="help")

# Help content pages
HELP_PAGES = [
    f"{hbold('/help')} – Show this help message.\n"
    f"{hbold('/set_channel')} – Add or update channel mapping.\n"
    f"{hbold('/list_channels')} – List all configured channels.\n"
    f"{hbold('/reload')} – Reload channel settings from config.",

    f"{hbold('/status')} – Show current bot status.\n"
    f"{hbold('/set_delay')} – Set forwarding delay.\n"
    f"{hbold('/start_id')} / {hbold('/end_id')} – Set message ID range.\n"
    f"{hbold('/duplicates')} – List unresolved duplicate titles.",

    "➕ Use the inline admin menu to add/delete channels.\n"
    "⚙️ Configure optional TMDB API for enhanced accuracy.\n"
    "📁 Bot supports forwarding messages with media & captions.\n"
    "🤖 Learning-based classification improves with usage."
]

@router.message(F.text == "/help")
async def show_help(message: Message):
    await message.answer(
        HELP_PAGES[0],
        parse_mode=ParseMode.HTML,
        reply_markup=get_help_keyboard(HELP_PAGES, 0)
    )

@router.callback_query(F.data.startswith("help:page:"))
async def paginate_help(callback: CallbackQuery):
    index = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        HELP_PAGES[index],
        parse_mode=ParseMode.HTML,
        reply_markup=get_help_keyboard(HELP_PAGES, index)
    )
    await callback.answer()

@router.callback_query(F.data == "help:noop")
async def noop(callback: CallbackQuery):
    await callback.answer("You're on this page.")
