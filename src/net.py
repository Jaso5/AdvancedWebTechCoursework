import requests

def get(
    url: str,
    method: str,
    query: list[str] | dict[str, str] | None = None,
    key: str | None = None
) -> requests.Response:
    # Construct base URL
    url = f"{url}/{method.lstrip('/')}"
    # Add query
    if type(query) == list:
        url += "?" + "&".join(query)
    elif type(query) == dict:
        url += "?" + "&".join(f"{k}={v}" for k, v in query.items())

    # Add api key
    headers = {}
    if key:
        headers["X-Api-Key"] = key

    print(f"GET {url}")
    return requests.get(url, headers=headers)
