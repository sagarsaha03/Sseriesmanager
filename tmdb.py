# tmdb.py

import aiohttp
import logging
from config import config

API_KEY = config.get("tmdb_api_key", "")

BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json;charset=utf-8"
}


async def search_tmdb(query):
    if not API_KEY:
        return None

    url = f"{BASE_URL}/search/multi?query={query}&include_adult=false&language=en-US&page=1"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=HEADERS) as response:
                data = await response.json()
                return data.get("results", [])
        except Exception as e:
            logging.exception(f"TMDB search failed: {e}")
            return None


async def get_tmdb_type(title: str) -> str:
    results = await search_tmdb(title)
    if not results:
        return "all_movies"

    top = results[0]
    media_type = top.get("media_type", "")
    origin_country = top.get("origin_country", [])
    original_language = top.get("original_language", "")

    if media_type == "tv":
        if original_language in ["hi"] or "IN" in origin_country:
            return "indian_webseries"
        if original_language in ["ko", "zh", "ja"]:
            return "asian_drama"
        return "hollywood_webseries"
    elif media_type == "movie":
        if original_language in ["hi"] or "IN" in origin_country:
            return "bollywood_movie"
        if original_language in ["ta", "te", "ml", "kn", "bn", "or"]:
            return "south_movie"
        return "hollywood_movie"
    else:
        return "all_movies"
