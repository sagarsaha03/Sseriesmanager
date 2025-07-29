# tmdb.py

import aiohttp
import asyncio

TMDB_API_KEY = None  # Will be set from bot command

def set_tmdb_key(key: str):
    global TMDB_API_KEY
    TMDB_API_KEY = key

async def search_tmdb(title: str):
    if not TMDB_API_KEY:
        return None

    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={title}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("results"):
                    return data["results"][0]
    return None

async def get_tmdb_info(title: str):
    try:
        result = await search_tmdb(title)
        if not result:
            return None

        name = result.get("title") or result.get("name")
        original_lang = result.get("original_language", "")
        media_type = result.get("media_type")

        if media_type == "tv":
            if original_lang == "hi":
                return "indian_webseries"
            elif original_lang in ["ko", "ja", "zh"]:
                return "asian_drama"
            else:
                return "hollywood_webseries"
        elif media_type == "movie":
            if original_lang == "hi":
                return "bollywood_movies"
            elif original_lang in ["ta", "te", "ml", "bn", "kn", "or"]:
                return "south_movies"
            elif original_lang == "en":
                return "hollywood_movies"
        return None
    except Exception:
        return None
