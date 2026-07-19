from cache import WeatherCache
from request import get_weather

cache = WeatherCache()

while True:
    city = ""
    while not city:
        print("Please enter a city, or type 'q' to quit")
        city = input("City name: ").strip().lower()
        if not city:
            print("Please enter a valid city name.")

    if city == "q":
        break

    data = cache.get(city)
    if data is None:
        data = get_weather(city)
        if data is not None:
            cache.set(city, data)
        else:
            continue

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
    print()