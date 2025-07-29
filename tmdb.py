# tmdb.py

import aiohttp
import logging
from config import load_config

config = load_config()
TMDB_API_KEY = config.tmdb_api_key

async def get_tmdb_data(title: str):
    if not TMDB_API_KEY:
        return None

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={title}"
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                results = data.get("results", [])
                if not results:
                    return None
                result = results[0]
                media_type = result.get("media_type")
                language = result.get("original_language", "")
                title = result.get("title") or result.get("name") or ""

                if media_type == "movie":
                    if language == "hi":
                        return ["bollywood movies", "all movies"]
                    elif language in ["ta", "te", "ml", "kn", "bn", "pa"]:
                        return ["south movies", "all movies"]
                    else:
                        return ["hollywood movies", "all movies"]

                elif media_type == "tv":
                    if language == "hi":
                        return ["indian webseries", "all webseries"]
                    elif language in ["ko", "ja", "zh", "th"]:
                        return ["asian drama", "all webseries"]
                    else:
                        return ["hollywood webseries", "all webseries"]

                return []
    except Exception as e:
        logging.error(f"TMDB error: {e}")
        return None
