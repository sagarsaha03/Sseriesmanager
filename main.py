import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import setup_db
from router_admin import admin_router
from router_forwarder import forward_router
from handlers.help import help_router

async def main():
    setup_db()
    bot = Bot(token="8016591770:AAFXBKlZS0HRlm1ThGhOKXmNymAHHvnNTDE")
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(admin_router)
    dp.include_router(forward_router)
    dp.include_router(help_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
