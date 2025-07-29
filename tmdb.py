# tmdb.py

import aiohttp
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

async def search_tmdb(query: str):
    if not TMDB_API_KEY:
        return None

    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            results = data.get("results", [])
            if not results:
                return None
            return results[0]  # Return top result

async def get_category_from_tmdb(query: str) -> str:
    result = await search_tmdb(query)
    if not result:
        return "unknown"

    media_type = result.get("media_type", "")
    original_language = result.get("original_language", "")

    if media_type == "movie":
        if original_language == "hi":
            return "bollywood"
        elif original_language in ["ta", "te", "ml", "kn", "bn", "mr", "pa", "or"]:
            return "south"
        else:
            return "hollywood"
    elif media_type == "tv":
        if original_language in ["hi"]:
            return "indian webseries"
        elif original_language in ["ko", "ja", "zh", "th"]:
            return "asian drama"
        else:
            return "hollywood webseries"
    else:
        return "unknown"
