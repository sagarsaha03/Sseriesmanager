import re
from aiogram.types import Message
from config import ADMIN_ID, load_config, save_config


def extract_title(text: str) -> str:
    """
    Extract a clean title from the message text or caption.
    Removes file extensions and quality tags.
    """
    if not text:
        return ""

    # Remove file extensions and resolutions
    cleaned = re.sub(r"\.(mkv|mp4|avi|webm)$", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(480p|720p|1080p|2160p|HDRip|BluRay|WEBRip|HEVC|x264|x265|ESubs|Hindi|Dual Audio)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)  # Remove special chars
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def format_log(action: str, target: str, status: str) -> str:
    return f"✅ <b>Action:</b> {action}\n<b>To:</b> {target}\n<b>Status:</b> {status}"


def is_admin(message: Message) -> bool:
    """Check if the message sender is the admin."""
    return message.from_user and message.from_user.id == ADMIN_ID


def save_channel_mapping(source_channel_id: int, category: str, main_target_id: int, backup_target_id: int):
    """Save channel mapping in the JSON config."""
    config = load_config()
    if "channels" not in config:
        config["channels"] = {}

    config["channels"][str(source_channel_id)] = {
        "category": category,
        "main": main_target_id,
        "backup": backup_target_id
    }

    save_config(config)


def get_configured_channels():
    """Get all configured channel mappings."""
    config = load_config()
    return config.get("channels", {})
