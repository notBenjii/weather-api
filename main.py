from cache import WeatherCache
from request import get_weather

city = ""
while not city:
    city = input("City name: ").strip().lower()
    if not city:
        print("Please enter a valid city name.")

cache = WeatherCache()
data = cache.get(city)
if data is None:
    data = get_weather(city)
    if data is not None:
        cache.set(city, data)

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