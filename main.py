# main.py
import asyncio
from aiogram import Bot, Dispatcher
from config import load_config
from router_admin import admin_router
from router_forwarder import forwarder_router
from help import help_router

config = load_config()
bot = Bot(token=config.bot_token, parse_mode="HTML")
dp = Dispatcher()

# Register all routers
dp.include_router(admin_router)
dp.include_router(forwarder_router)
dp.include_router(help_router)

async def main():
    print("🤖 Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
