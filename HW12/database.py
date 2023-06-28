from typing import List, Tuple, Any
import psycopg2


class WeatherDatabase:
    def __init__(self, dbname="weather", user="postgres", password="ffarzam_1992", host='localhost', port='5432'):
        self.conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def create_tables(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                            id BIGSERIAL PRIMARY KEY NOT NULL,
                            username VARCHAR(50) NOT NULL UNIQUE,
                            password TEXT NOT NULL);""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Requests(
                            id BIGSERIAL PRIMARY KEY NOT NULL,
                            user_id BIGINT NOT NULL,
                            city VARCHAR(50) NOT NULL,
                            request_time TIMESTAMP,
                            status_code BIGINT,
                            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE);""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Responses(
                            id BIGSERIAL PRIMARY KEY NOT NULL,
                            request_id BIGINT NOT NULL UNIQUE,
                            city VARCHAR(50) NOT NULL,
                            temperature DECIMAL NOT NULL,
                            feels_like_temperature DECIMAL NOT NULL,
                            last_updated_time TIMESTAMP NOT NULL,
                            FOREIGN KEY (request_id) REFERENCES Requests(id) ON DELETE CASCADE ON UPDATE CASCADE);""")
        self.conn.commit()

    def set_user(self, my_username, my_password):
        self.cur.execute(
            f"""INSERT INTO Users(username,password) VALUES ('{my_username}',crypt('{my_password}', gen_salt('bf')));""")
        self.conn.commit()

    def login_user(self, my_username, my_password):
        self.cur.execute(
            f"""SELECT (password = crypt('{my_password}', password)) AS pwd_match FROM Users WHERE username ='{my_username}';""")
        result = self.cur.fetchone()
        if result is None:
            result = (False,)
        return result[0]

    def check_username(self, username):
        self.cur.execute(
            f"""SELECT username FROM Users WHERE username ='{username}';""")
        result = self.cur.fetchone()
        return result

    def get_user(self, my_username):
        self.cur.execute(
            f"""SELECT id 
            FROM Users WHERE username ='{my_username}';""")
        result = self.cur.fetchone()
        return result

    def save_request_data(self, user_id, city_name: str, request_time: str, status_code: str) -> None:
        self.cur.execute(f"""INSERT INTO requests(user_id,city,request_time,status_code) 
                            VALUES ({user_id},'{city_name}', '{request_time}','{status_code}');""")
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

    def get_last_hour_requests(self) -> List[Tuple[Any, ...]]:
        self.cur.execute('''SELECT id, city, TO_CHAR(request_time, 'YYYY-MM-DD HH24:MI:SS') as request_time
                            FROM requests 
                            WHERE AGE(NOW(),request_time) < INTERVAL '1 Hour'
                            ORDER BY request_time DESC;''')
        result = self.cur.fetchall()
        return result

    def get_city_request_count(self) -> List[Tuple[Any, ...]]:
        self.cur.execute("SELECT city, COUNT(*) FROM requests GROUP BY city ORDER BY COUNT(*) DESC")
        result = self.cur.fetchall()
        return result

    def cache(self, city_name):
        self.cur.execute(f'''SELECT id, city,temperature,feels_like_temperature,last_updated_time
                            FROM responses
                            WHERE AGE(NOW(),last_updated_time) < INTERVAL '10 MINUTE' AND city= '{city_name}'
                            ORDER BY last_updated_time DESC
                            LIMIT 1;''')
        result = self.cur.fetchone()
        return result

    def close(self) -> None:
        self.cur.close()
        self.conn.close()
