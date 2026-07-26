import threading
from textwrap import dedent

import customtkinter as ctk
from cache import WeatherCache
from request import get_weather

class WeatherApp:
    WINDOW_SIZE = "700x450"
    ANIMATION_INTERVAL_MS = 400

    def __init__(self):
        self.searching = False
        self.cache = WeatherCache()

        self.app = ctk.CTk()
        self.app.title("Weather App")
        self.app.geometry(self.WINDOW_SIZE)
        self.app.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self._build_widgets()

    def _build_widgets(self):
        self.title_label = ctk.CTkLabel(self.app, text="Weather App", font=("Arial", 30))
        self.title_label.pack(pady=20)

        self.city_entry = ctk.CTkEntry(self.app, placeholder_text="Enter city name")
        self.city_entry.pack(pady=(10, 0))
        self.default_border_color = self.city_entry.cget("border_color")

        self.city_error_label = ctk.CTkLabel(self.app, text="", font=("Arial", 12), text_color="red")
        self.city_error_label.pack(pady=(0, 10))

        self.search_button = ctk.CTkButton(self.app, text="Search", command=self.search_weather)
        self.search_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(self.app, text="", font=("Arial", 16), justify="left")
        self.result_label.pack(pady=10)

        self.city_entry.bind("<Return>", self.search_weather)

    def search_weather(self, event=None):
        if self.search_button.cget("state") == "disabled":
            return

        self.search_button.configure(state="disabled")
        city = self.city_entry.get().strip().lower()

        if not city:
            self.city_entry.configure(border_color="red")
            self.city_error_label.configure(text="Please enter a valid city name.")
            self.search_button.configure(state="normal")
            return

        self.city_entry.configure(border_color=self.default_border_color)
        self.city_error_label.configure(text="")

        self.searching = True
        self.app.after(self.ANIMATION_INTERVAL_MS, self.animate_loading, "")

        thread = threading.Thread(target=self.fetch_weather_data, args=(city,))
        thread.start()

    def fetch_weather_data(self, city):
        data = self.cache.get(city)
        if data is None:
            data = get_weather(city)
            if data is not None:
                self.cache.set(city, data)

        self.app.after(0, self.update_result_label, data)

    def update_result_label(self, data):
        self.searching = False

        if data is not None:
            self.result_label.configure(text=self._format_weather_text(data))
        else:
            self.result_label.configure(text="Something went wrong...")

        self.search_button.configure(state="normal")

    @staticmethod
    def _format_weather_text(data) -> str:
        date = data["current"]["last_updated"]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        wind = data["current"]["wind_kph"]
        cloud_percentage = data["current"]["cloud"]

        return dedent(f"""
            Last updated: {date}

            Temperature: {temp}°C

            Condition: {condition}

            Wind: {wind} kph

            Cloud coverage: {cloud_percentage}%
        """).strip()

    def animate_loading(self, dots=""):
        if not self.searching:
            return

        self.result_label.configure(text=f"Loading{dots}")

        if dots == "...":
            new_dots = ""
        else:
            new_dots = dots + "."

        self.app.after(self.ANIMATION_INTERVAL_MS, self.animate_loading, new_dots)

    def run(self):
        self.app.mainloop()