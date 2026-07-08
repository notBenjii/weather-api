import json
import time

class WeatherCache:
    def __init__(self, filename="weather_cache.json", max_age_seconds=600):
        self.filename = filename
        self.max_age_seconds = max_age_seconds
        self.cache = self._load()

    def _load(self) -> dict:
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save(self):
        with open(self.filename, "w") as f:
            json.dump(self.cache, f)

    def is_valid(self, city: str) -> bool:
        if city not in self.cache:
            return False
        age = time.time() - self.cache[city]["timestamp"]
        return age < self.max_age_seconds

    def get(self, city: str):
        if self.is_valid(city):
            return self.cache[city]["data"]
        return None

    def set(self, city: str, data: dict):
        self.cache[city] = {
            "timestamp": time.time(),
            "data": data
        }
        self._save()