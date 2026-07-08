import requests
from keys import API_KEY

city = ""

while not city:
    city = input("City name: ").strip()
    if not city:
        print("Please enter a valid city name.")

url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Could not fetch weather data: {e}")
    exit()

if response.status_code != 200:
    error_msg = response.json().get("error", {}).get("message", "Unknown error")
    print(f"Error: {error_msg}")
    exit()

data = response.json()

date = data["current"]["last_updated"]
temp = data["current"]["temp_c"]
condition = data["current"]["condition"]["text"]
wind = data["current"]["wind_kph"]
cloud_percentage = data["current"]["cloud"]

print(f"Last updated {date}")
print(f"Temperature: {temp}°C")
print(f"Condition: {condition}")
print(f"Wind: {wind} kph")
print(f"Cloud coverage: {cloud_percentage}%")