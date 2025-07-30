from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import help_keyboard

help_router = Router()

@help_router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "📚 SSeriesManager Bot Commands",
        reply_markup=help_keyboard()
    )

@help_router.callback_query(F.data.startswith("help_"))
async def help_pagination(callback: CallbackQuery):
    data = callback.data.split("_")
    action = data[1]
    
    if action == "page":
        page = int(data[2])
        await callback.message.edit_reply_markup(
            reply_markup=help_keyboard(page)
        )
        await callback.answer()
    else:
        command = data[1]
        await callback.answer(f"Selected command: /{command}")
