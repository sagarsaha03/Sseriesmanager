from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router(name=__name__)

# Help pages
help_pages = [
    """🔰 <b>SSeriesManager Bot Help</b> 🔰

Use the following commands to control the bot:
    
🛠️ Admin Commands:
/addchannel - Add source/target/backup channel
/setdelay - Set delay in seconds
/settmdb - Set TMDB API key
/status - Check current configuration
/reload - Reload config
/help - Show help with buttons

Use the inline buttons to navigate pages. 👇""",
    """📡 <b>Forwarding Rules</b>:

• All Movies → all types of movies (Bollywood, Hollywood, South)
• Bollywood Movies → only if original release language is Hindi
• Hollywood Movies → non-Indian movies
• South Movies → Indian regional (Tamil, Telugu, Bengali, etc.)
• All Webseries → all types of series
• Indian Webseries → only Indian series
• Hollywood Webseries → international including Asian drama
• Asian Drama → Korean, Japanese, Thai, etc.
• Anime → All animated movies or series

✅ “All Movies” and “All Webseries” are mandatory for each relevant post.""",
    """⚙️ <b>Configuration via Commands</b>:

/addchannel source <name> <channel_id>
/addchannel main <category> <channel_id>
/addchannel backup <category> <channel_id>

/setdelay <seconds>
/settmdb <your_tmdb_key>
/reload

Example:
/addchannel main south -1001234567890

⏱️ Delay is the wait time between forwards (in seconds).

Use /status to check current configuration.

Need more help? Contact admin.
"""
]

def get_help_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if page > 0:
        builder.button(text="⬅️ Prev", callback_data=f"help_page:{page-1}")
    if page < len(help_pages) - 1:
        builder.button(text="Next ➡️", callback_data=f"help_page:{page+1}")
    builder.adjust(2)
    return builder.as_markup()

@router.message(F.text == "/help")
async def send_help(message: Message):
    page = 0
    await message.answer(help_pages[page], parse_mode=ParseMode.HTML, reply_markup=get_help_keyboard(page))

@router.callback_query(F.data.startswith("help_page:"))
async def paginate_help(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_text(help_pages[page], parse_mode=ParseMode.HTML, reply_markup=get_help_keyboard(page))
    await callback.answer()
