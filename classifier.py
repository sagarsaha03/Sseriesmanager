# classifier.py

import re

def classify_content(message):
    text = (message.text or "") + " " + (message.caption or "")
    text = text.lower()

    # Anime detection
    if "anime" in text:
        return "anime"

    # Asian Drama detection
    if any(x in text for x in ["korean", "japanese", "chinese", "thai", "asian drama"]):
        return "asian_drama"

    # Webseries detection
    if "webseries" in text or "web series" in text:
        if "indian" in text or "hindi" in text:
            return "indian_webseries"
        elif any(x in text for x in ["english", "hollywood", "korean", "japanese", "chinese", "asian"]):
            return "hollywood_webseries"
        else:
            return "all_webseries"

    # Movie detection
    if "movie" in text or "film" in text:
        if "south" in text or re.search(r"\b(tamil|telugu|malayalam|bengali|odia|kannada)\b", text):
            return "south_movies"
        elif "hollywood" in text or "english" in text:
            return "hollywood_movies"
        elif "hindi" in text or "bollywood" in text:
            return "bollywood_movies"
        else:
            return "all_movies"

    # Default fallback
    return "all_movies"
