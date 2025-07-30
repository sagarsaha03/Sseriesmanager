import re

def classify_content(text):
    patterns = {
        "SERIES": r"\b(SEASON|S\d{1,2}|EPISODE|EP|SERIES)\b",
        "MOVIE": r"\b(MOVIE|FILM|CINEMA|MOV)\b",
        "DOCUMENTARY": r"\b(DOCUMENTARY|DOC|DOCU)\b",
        "ANIME": r"\b(ANIME|MANGA|EPISODE)\b",
        "SPORTS": r"\b(SPORTS|SOCCER|FOOTBALL|BASKETBALL|MATCH)\b",
    }
    
    if not text:
        return "OTHER"
    
    text = text.upper()
    for category, pattern in patterns.items():
        if re.search(pattern, text):
            return category
    return "OTHER"
