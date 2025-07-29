# main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import load_config
from router_admin import admin_router
from router_forwarder import forwarder_router
from handlers.help import help_router

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config
config = load_config()

# Initialize bot and dispatcher
bot = Bot(token=config.bot_token, parse_mode="HTML")
dp = Dispatcher()

# Register routers
dp.include_router(admin_router)
dp.include_router(forwarder_router)
dp.include_router(help_router)

async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    

