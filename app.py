import threading
import customtkinter as ctk
from cache import WeatherCache
from request import get_weather

searching = False
cache = WeatherCache()

app = ctk.CTk()
app.title("Weather App")
app.geometry("700x450")
app.resizable(False, False)
ctk.set_appearance_mode("dark")

title_label = ctk.CTkLabel(app, text="Weather App", font=("Arial", 30))
title_label.pack(pady=20)

city_entry = ctk.CTkEntry(app, placeholder_text="Enter city name")
city_entry.pack(pady=(10, 0))
default_border_color = city_entry.cget("border_color")

city_error_label = ctk.CTkLabel(app, text="", font=("Arial", 12), text_color="red")
city_error_label.pack(pady=(0, 10))

def search_weather(event = None):
    if search_button.cget("state") == "disabled":
        return

    search_button.configure(state="disabled")
    city = city_entry.get().strip().lower()

    if not city:
        city_entry.configure(border_color="red")
        city_error_label.configure(text="Please enter a valid city name.")
        search_button.configure(state="normal")
        return

    city_entry.configure(border_color=default_border_color)
    city_error_label.configure(text="")

    global searching
    searching = True
    app.after(400, animate_loading , "")

    thread = threading.Thread(target=fetch_weather_data, args=(city,))
    thread.start()

def fetch_weather_data(city):
    data = cache.get(city)
    if data is None:
        data = get_weather(city)
        if data is not None:
            cache.set(city, data)

    app.after(0, update_result_label, data)

def update_result_label(data):
    global searching
    searching = False

    if data is not None:
        date = data["current"]["last_updated"]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        wind = data["current"]["wind_kph"]
        cloud_percentage = data["current"]["cloud"]

        result_label.configure(text=f"""
        Last updated: {date}

        Temperature: {temp}°C

        Condition: {condition}

        Wind: {wind} kph

        Cloud coverage: {cloud_percentage}%
        """)
    else:
        result_label.configure(text="Something went wrong...")

    search_button.configure(state="normal")

def animate_loading(dots = ""):
    if not searching:
        return

    result_label.configure(text=f"Loading{dots}")

    if dots == "...":
        new_dots = ""
    else:
        new_dots = dots + "."

    app.after(400, animate_loading, new_dots)

search_button = ctk.CTkButton(app, text="Search", command=search_weather)
search_button.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 16), justify="left")
result_label.pack(pady=10)

city_entry.bind("<Return>", search_weather)
app.mainloop()

