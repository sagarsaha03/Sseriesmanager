# classifier.py

CATEGORIES = {
    "all movies": ["movie", "film", "720p", "1080p"],
    "bollywood movies": ["hindi movie", "bollywood"],
    "hollywood movies": ["english movie", "hollywood"],
    "south movies": ["telugu", "tamil", "malayalam", "kannada"],
    "all webseries": ["webseries", "series", "season"],
    "indian webseries": ["hindi webseries", "ullu", "voot", "zee5", "mx player"],
    "hollywood webseries": ["netflix", "amazon", "hbo", "english webseries"],
    "asian drama": ["kdrama", "k-drama", "jdrama", "cdrama", "thai", "korean"],
    "anime": ["anime", "animated", "cartoon"]
}

def classify_content(text: str) -> list:
    matches = []
    text_lower = text.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in text_lower:
                matches.append(category)
                break

    # Ensure “all movies” and “all webseries” are always included
    if any(cat for cat in matches if "movie" in cat):
        if "all movies" not in matches:
            matches.append("all movies")
    if any(cat for cat in matches if "webseries" in cat or "drama" in cat or "anime" in cat):
        if "all webseries" not in matches:
            matches.append("all webseries")

    return matches
