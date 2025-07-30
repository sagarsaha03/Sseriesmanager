import sqlite3
import re
import asyncio
from config import Config, get_channel, bot
from classifier import classify_content
from tmdb import get_tmdb_info
from keyboards import duplicate_keyboard
from datetime import datetime

async def process_and_forward(message: Message):
    # Get message content
    text = message.caption or message.text or ""
    
    # Clean text
    replace_rules = Config.get('domain_replace') or ''
    if '->' in replace_rules:
        old, new = replace_rules.split('->')
        text = text.replace(old.strip(), new.strip())
    
    # Add custom message
    custom_msg = Config.get('custom_message') or ''
    if custom_msg:
        text += f"\n\n{custom_msg}"
    
    # Classification
    category = classify_content(text)
    
    # Use TMDB if enabled
    tmdb_enabled = Config.get('tmdb_enabled') == 'true'
    tmdb_data = None
    if tmdb_enabled:
        tmdb_data = get_tmdb_info(text)
        if tmdb_data:
            category = tmdb_data.get('type', category)
            if tmdb_data.get('title') and tmdb_data.get('year'):
                text = f"{tmdb_data['title']} ({tmdb_data['year']})\n\n" + text
    
    # Get target channel
    target = get_channel('target')
    if not target:
        return
    
    # Forward message
    try:
        forwarded = await bot.forward_message(
            chat_id=target[0],
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        
        # Save to database
        conn = sqlite3.connect("sseriesmanager.db")
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO messages (source_msg_id, target_msg_id, channel_id, title)
        VALUES (?, ?, ?, ?)
        """, (message.message_id, forwarded.message_id, target[0], text[:100]))
        conn.commit()
        conn.close()
        
        # Check duplicates
        await check_duplicates(forwarded, text[:100])
        
        # Log action
        await log_action(f"✅ Forwarded: {text[:50]}...", category)
    except Exception as e:
        await log_action(f"❌ Forward failed: {e}", "ERROR")

async def check_duplicates(message: Message, title: str):
    conn = sqlite3.connect("sseriesmanager.db")
    cur = conn.cursor()
    cur.execute("""
    SELECT id, source_msg_id FROM messages 
    WHERE channel_id = ? AND title = ? AND id != ?
    """, (str(message.chat.id), title, message.message_id))
    
    duplicate = cur.fetchone()
    if duplicate:
        # Save duplicate record
        cur.execute("""
        INSERT INTO duplicates (original_msg_id, duplicate_msg_id, channel_id)
        VALUES (?, ?, ?)
        """, (duplicate[1], message.message_id, str(message.chat.id)))
        conn.commit()
        
        # Notify admin
        log_channel = get_channel('log')
        if log_channel:
            await bot.send_message(
                chat_id=log_channel[0],
                text=f"⚠️ Duplicate detected!\nTitle: {title[:50]}...",
                reply_markup=duplicate_keyboard(duplicate[0], message.message_id)
            )
    conn.close()

async def log_action(message: str, category: str = "INFO"):
    log_channel = get_channel('log')
    if not log_channel:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{category}]\n{message}"
    
    try:
        await bot.send_message(chat_id=log_channel[0], text=log_msg)
    except:
        pass
