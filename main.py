# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import load_config
from router_admin import admin_router
from router_forwarder import forwarder_router
from handlers.help import help_router

config = load_config()
bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_routers(admin_router, forwarder_router, help_router)

async def main():
    print("🤖 SSeriesManager bot started.")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
