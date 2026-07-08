import requests
from keys import API_KEY

def get_weather(city: str) -> dict | None:
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch weather data: {e}")
        if e.response is not None:
            error_msg = e.response.json().get("error", {}).get("message", "Unknown error")
            print(f"Error: {error_msg}")
        return None

    return response.json()