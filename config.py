import sqlite3
import asyncio
from pathlib import Path
from aiogram import Bot

DB_PATH = Path("sseriesmanager.db")
ADMIN_ID = 1588777572
BOT_TOKEN = "8016591770:AAFXBKlZS0HRlm1ThGhOKXmNymAHHvnNTDE"

bot = Bot(token=BOT_TOKEN)

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Configuration table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    # Channels table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT NOT NULL UNIQUE,
        channel_name TEXT,
        role TEXT CHECK(role IN ('source', 'log', 'target', 'backup'))
    )
    """)
    
    # Forwarding rules
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pattern TEXT NOT NULL,
        category TEXT NOT NULL,
        main_channel TEXT,
        backup_channel TEXT
    )
    """)
    
    # Message tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_msg_id INTEGER NOT NULL,
        target_msg_id INTEGER,
        channel_id TEXT NOT NULL,
        title TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Duplicate detection
    cur.execute("""
    CREATE TABLE IF NOT EXISTS duplicates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_msg_id INTEGER NOT NULL,
        duplicate_msg_id INTEGER NOT NULL,
        channel_id TEXT NOT NULL,
        status TEXT DEFAULT 'pending'
    )
    """)
    
    # Set default config
    cur.execute("INSERT OR IGNORE INTO config VALUES ('tmdb_enabled', 'false')")
    cur.execute("INSERT OR IGNORE INTO config VALUES ('forward_delay', '0')")
    cur.execute("INSERT OR IGNORE INTO config VALUES ('domain_replace', 'https://old.domain.com->https://new.domain')")
    cur.execute("INSERT OR IGNORE INTO config VALUES ('custom_message', '🔰 Powered by SSeriesManager')")
    
    conn.commit()
    conn.close()

class Config:
    @staticmethod
    def get(key):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT value FROM config WHERE key=?", (key,))
        result = cur.fetchone()
        conn.close()
        return result[0] if result else None

    @staticmethod
    def set(key, value):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()

async def set_channel(role, channel_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        chat = await bot.get_chat(channel_id)
        channel_name = chat.title
    except:
        channel_name = "Unknown"
    
    cur.execute("""
    INSERT OR REPLACE INTO channels (channel_id, channel_name, role)
    VALUES (?, ?, ?)
    """, (channel_id, channel_name, role))
    conn.commit()
    conn.close()

def get_channel(role):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT channel_id, channel_name FROM channels WHERE role=?", (role,))
    result = cur.fetchone()
    conn.close()
    return result
