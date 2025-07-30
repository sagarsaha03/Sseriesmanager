# utils.py

import re
import logging
from aiogram.types import Message


def extract_title_from_text(text: str) -> str:
    """
    Extracts the main title from a forwarded message's text or caption.
    """
    # Remove common patterns like resolution, quality, codec, etc.
    clean_text = re.sub(
        r"[\[\(](1080p|720p|480p|HDRip|WEBRip|HEVC|x265|x264|ESubs|Dual Audio|Multi Audio|Hindi|English|Japanese|Tamil|Telugu|Malayalam|Kannada|Chinese|Punjabi|ORG-2\.0)[\]\)]",
        "", text, flags=re.IGNORECASE)

    # Remove extra brackets and years
    clean_text = re.sub(r"\{.*?\}|\[.*?\]|\(.*?\)", "", clean_text)
    clean_text = re.sub(r"\b(19|20)\d{2}\b", "", clean_text)

    # Remove special characters and extra spaces
    title = re.sub(r"[^A-Za-z0-9\s:,'\-]", "", clean_text)
    title = re.sub(r"\s+", " ", title).strip()

    return title


def format_forward_log(title: str, status: str, target: str):
    return f"📦 **Forwarded** `{title}`\n✅ Status: `{status}`\n📤 Sent to: `{target}`"


def is_duplicate(title: str, channel_id: int, database: dict) -> int | None:
    """
    Check if a title exists in the same channel in the database.
    Return original message_id if duplicate exists.
    """
    if channel_id not in database:
        return None
    for msg_id, saved_title in database[channel_id].items():
        if saved_title.lower() == title.lower():
            return msg_id
    return None


def save_title(title: str, channel_id: int, message_id: int, database: dict):
    if channel_id not in database:
        database[channel_id] = {}
    database[channel_id][message_id] = title
    logging.info(f"Saved title for duplicate check: {title} -> {message_id}")
