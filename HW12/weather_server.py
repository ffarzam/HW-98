import requests as rq
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qsl, urlparse


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


class MyWeatherServer(BaseHTTPRequestHandler):

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        query_data = self.query_data()
        choice = query_data["city"]
        weather_info = get_city_weather(choice)
        weather_info_json = json.dumps(weather_info)
        self.wfile.write(weather_info_json.encode("utf-8"))


def start_server() -> None:
    HOST = "192.168.1.167"
    # HOST="192.168.1.110"
    PORT = 8080

    server = HTTPServer((HOST, PORT), MyWeatherServer)
    print("Server listening on")
    server.serve_forever()
    server.server_close()
    print("Server closed")


if __name__ == "__main__":
    start_server()