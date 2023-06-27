from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qsl, urlparse
from actions import *
import requests as rq
from database import WeatherDatabase


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
            return {"status code": response.status_code, "weather_info": weather_info}

        return {"status code": response.status_code, "weather_info": response.json()}


class MyWeatherServer(BaseHTTPRequestHandler):

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        query_data = self.query_data()
        choice = query_data["city"]
        username = query_data["user"]
        weather_info = get_city_weather(choice)
        weather_info_json = json.dumps(weather_info["weather_info"])
        self.send_response(weather_info["status code"])
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(weather_info_json.encode("utf-8"))
        user_id = get_user_id(database, username)
        if weather_info["status code"] == 200:
            save_request(database, user_id, choice)
            save_response(database, choice, weather_info["weather_info"])
        else:
            save_request(database, user_id, choice)

    def do_POST(self):

        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        post_body_dict = json.loads(post_body)
        if post_body_dict["action"] == "signin":
            save_user(database, post_body_dict["username"], post_body_dict["password"])
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # self.wfile.write(post_body)
        elif post_body_dict["action"] == "login":
            state = check_login_user(database, post_body_dict["username"], post_body_dict["password"])
            state_json = json.dumps({"status": state})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(state_json.encode('utf-8'))


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
    database = WeatherDatabase()
    database.create_tables()
    start_server()
    database.close()
