from typing import Final
from dataclasses import dataclass
from requests_cache import CachedSession

URL: Final = "https://animechan.vercel.app/api/random"

session = CachedSession(
    cache_name = 'cache/anime_cache',
    expire_after = 600
)

@dataclass
class Quote:
    anime: str = None
    character: str = None
    quote: str = None

def get_response():
    response = session.get(URL)

    try: 
        json: dict = response.json()
        quote = Quote(**json)

        print(f'"{quote.quote}"')
        print(f"- {quote.character} ({quote.anime})")
    except Exception as e:
        print(f'{response.status_code} - {e}')

    if __name__ == '__main__':
        get_response()