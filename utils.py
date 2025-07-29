# utils.py

import re

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
