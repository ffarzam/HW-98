import requests as rq
from datetime import datetime


class ConnectionManager:
    def __init__(self, final_url: str):
        self.final_url = final_url

    def __enter__(self):
        self.file = rq.get(self.final_url)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()


def get_city_weather(city: str) -> dict:
    weather_info = {}
    RAW_URL = "http://api.openweathermap.org/data/2.5/weather"
    API_KEY = "3eb2381ac662acb4defa744088a680ba"
    final_url = RAW_URL + "?q=" + city + "&appid=" + API_KEY + "&units=metric"

    with ConnectionManager(final_url) as response:
        if response:
            weather_info["temperature"] = response.json()["main"]["temp"]
            weather_info["feels_like"] = response.json()["main"]["feels_like"]
            weather_info["last_updated"] = datetime.fromtimestamp(response.json()["dt"]).strftime("%Y-%m-%d %H:%M:%S")
            return weather_info
    return response.json()