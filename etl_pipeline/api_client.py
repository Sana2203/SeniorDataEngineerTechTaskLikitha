import requests

POSTS_URL = "https://jsonplaceholder.typicode.com/posts"
USERS_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_json(url: str, timeout: int = 10) -> list[dict]:
    """Fetch JSON list data from a given API endpoint."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list from {url}, got {type(data).__name__}")
    return data