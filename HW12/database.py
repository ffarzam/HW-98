import psycopg2


class WeatherDatabase:
    def __init__(self, dbname="weather", user="postgres", password="ffarzam_1992", host='localhost', port='5432'):
        self.conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Requests(
                            id BIGSERIAL PRIMARY KEY NOT NULL,
                            city VARCHAR(50) NOT NULL,
                            request_time TIMESTAMP);""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Responses(
                            id BIGSERIAL PRIMARY KEY NOT NULL,
                            request_id BIGINT NOT NULL UNIQUE,
                            city VARCHAR(50) NOT NULL,
                            temperature DECIMAL NOT NULL,
                            feels_like_temperature DECIMAL NOT NULL,
                            last_updated_time TIMESTAMP NOT NULL,
                            FOREIGN KEY (request_id) REFERENCES Requests(id));""")
        self.conn.commit()

    def save_request_data(self, city_name: str, request_time: str) -> None:
        self.cur.execute("""INSERT INTO requests(city,request_time) VALUES (%s,%s);""", (city_name, request_time))
        self.conn.commit()

    def save_response_data(self, city_name: str, response_data: dict) -> None:
        self.cur.execute(f'''INSERT INTO responses(request_id,city,temperature,feels_like_temperature,last_updated_time)
        VALUES (
        (SELECT last_value FROM requests_id_seq),
        '{city_name}',
        {response_data['temperature']},
        {response_data['feels_like']},
        '{response_data['last_updated']}');''')
        self.conn.commit()
