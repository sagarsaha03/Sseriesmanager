# classifier.py

import re

def classify_title(title: str) -> str:
    title = title.lower()

    # Priority order matters
    if "anime" in title:
        return "anime"
    if any(x in title for x in ["webseries", "web series", "series", "tvf", "kdrama", "jdrama", "cdrama", "drama"]):
        if any(x in title for x in ["korean", "chinese", "japanese", "thai", "asian"]):
            return "asian_drama"
        if any(x in title for x in ["netflix", "amazon", "prime", "hotstar", "voot", "zee5", "mx", "ullu", "tvf", "altbalaji"]):
            return "indian_webseries"
        return "hollywood_webseries"
    if any(x in title for x in ["hindi", "bollywood", "punjabi", "gujarati", "bhojpuri", "marathi"]):
        return "bollywood_movie"
    if any(x in title for x in ["english", "hollywood"]):
        return "hollywood_movie"
    if any(x in title for x in ["malayalam", "tamil", "telugu", "kannada", "odia", "bengali"]):
        return "south_movie"
    return "all_movies"
