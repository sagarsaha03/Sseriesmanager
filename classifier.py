# classifier.py

import re

# Define categories and their keywords
CATEGORIES = {
    "bollywood movies": ["bollywood", "hindi movie"],
    "hollywood movies": ["hollywood", "english movie"],
    "south movies": ["south", "telugu", "tamil", "malayalam", "kananda"],
    "anime": ["anime", "animation", "cartoon"],
    "indian webseries": ["web series", "webseries", "indian series", "ullu", "voot", "alt balaji"],
    "hollywood webseries": ["netflix", "marvel", "dc", "english series", "hbo"],
    "asian drama": ["kdrama", "cdrama", "jdrama", "korean", "thai", "chinese"],
    "all movies": ["movie"],
    "all webseries": ["series", "webseries"]
}

# Define priority for fallback matching (when multiple matches)
CATEGORY_PRIORITY = [
    "anime",
    "asian drama",
    "bollywood movies",
    "south movies",
    "hollywood movies",
    "indian webseries",
    "hollywood webseries",
    "all movies",
    "all webseries"
]

def classify_message(message):
    """Classify the message based on title or caption."""
    text = ""
    if message.text:
        text = message.text.lower()
    elif message.caption:
        text = message.caption.lower()

    found_categories = []

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                found_categories.append(category)
                break  # Stop checking this category if a keyword matched

    if not found_categories:
        return None

    # Return the highest priority category match
    for cat in CATEGORY_PRIORITY:
        if cat in found_categories:
            return cat

    return found_categories[0]
