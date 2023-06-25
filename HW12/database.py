import psycopg2


class WeatherDatabase:
    def __init__(self, dbname="weather", user="postgres", password="ffarzam_1992", host='localhost', port='5432'):
        self.conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
