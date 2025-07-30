import sqlite3
from pathlib import Path

DB_PATH = Path("sseriesmanager.db")
ADMIN_ID = 1588777572

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
        main_channel
