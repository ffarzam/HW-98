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

    def get_request_count(self) -> int:
        self.cur.execute('''SELECT COUNT(*) FROM requests''')
        result = self.cur.fetchone()
        return result[0]

    def get_successful_request_count(self) -> int:
        self.cur.execute('''SELECT COUNT(*) FROM responses''')
        result = self.cur.fetchone()
        return result[0]

    def get_last_hour_requests(self) -> list:
        self.cur.execute('''SELECT city, TO_CHAR(request_time, 'YYYY-MM-DD HH24:MI:SS')
                            FROM requests 
                            WHERE AGE(NOW(),request_time) < INTERVAL '1 Hour';''')
        result = self.cur.fetchall()
        return result

    def get_city_request_count(self) -> list:
        self.cur.execute("SELECT city, COUNT(*) FROM requests GROUP BY city")
        result = self.cur.fetchall()
        return result
