# main.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from router_admin import admin_router
from router_forwarder import forwarder_router
from handlers import help_handler

async def main():
    config = load_config()
    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        admin_router,
        forwarder_router,
        help_handler.router
    )

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
