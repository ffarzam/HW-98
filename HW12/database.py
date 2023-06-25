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
