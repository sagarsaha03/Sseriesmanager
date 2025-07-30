# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from router_admin import router as admin_router
from router_forwarder import router as forwarder_router
from handlers.help import router as help_router

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(admin_router)
    dp.include_router(forwarder_router)
    dp.include_router(help_router)

    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
