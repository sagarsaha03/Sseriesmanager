from aiogram import Router
from aiogram.types import Message
from config import Config, get_channel
import utils
import asyncio
import re

forward_router = Router()

@forward_router.channel_post()
async def handle_channel_post(message: Message):
    # Check if from source channel
    source_channel = get_channel('source')
    if not source_channel or str(message.chat.id) != source_channel[0]:
        return
    
    # Apply delay if configured
    delay = int(Config.get('forward_delay') or 0)
    if delay > 0:
        await asyncio.sleep(delay)
    
    await utils.process_and_forward(message)
