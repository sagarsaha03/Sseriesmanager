import requests

TMDB_API_KEY = "YOUR_TMDB_API_KEY"  # Replace with your actual key

def get_tmdb_info(title):
    if not TMDB_API_KEY or TMDB_API_KEY == "YOUR_TMDB_API_KEY":
        return None
        
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={title[:50]}"
    try:
        response = requests.get(url, timeout=10)
        results = response.json().get('results', [])
        if results:
            return {
                'type': results[0].get('media_type', 'unknown').upper(),
                'title': results[0].get('title') or results[0].get('name'),
                'year': results[0].get('release_date', '')[:4] if results[0].get('release_date') else ''
            }
    except Exception as e:
        print(f"TMDB Error: {e}")
    return None
