import json
import os
from typing import Dict

DB_FILE = "data/seen_titles.json"

def load_database() -> Dict[int, Dict[int, str]]:
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_database(db: Dict[int, Dict[int, str]]):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
