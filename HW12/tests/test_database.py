import pytest
from HW12.database import WeatherDatabase
import datetime


@pytest.fixture
def db():
    db = WeatherDatabase()
    yield db
    db.close()


def test_create_tables(db):
    db.create_tables()
    cursor = db.cur

    cursor.execute('''SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';''')

    tables = [table[0] for table in cursor.fetchall()]

    assert 'requests' in tables
    assert 'responses' in tables


def test_save_request_data(db):
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.save_request_data(city_name, request_time)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM requests ORDER BY id DESC")
    row = cursor.fetchone()

    assert row[1] == city_name
    assert row[2] == datetime.datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S")
    cursor.execute('''SELECT last_value FROM requests_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM requests WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('requests_id_seq', {id_num}, false);''')
    db.conn.commit()


def test_save_response_data(db):
    cursor = db.conn.cursor()
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""INSERT INTO requests(city,request_time) VALUES (%s,%s);""", (city_name, request_time))
    db.conn.commit()

    city_name = "rasht"
    temperature = 30
    feels_like_temperature = 28.4
    last_update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = {'temperature': temperature, 'feels_like': feels_like_temperature, 'last_updated': last_update_time}

    db.save_response_data(city_name, weather_info)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM responses ORDER BY id DESC")
    row = cursor.fetchone()

    assert row[2] == city_name
    assert row[3] == temperature
    assert float(row[4]) == feels_like_temperature
    assert row[5] == datetime.datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")
    cursor.execute('''SELECT last_value FROM responses_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM responses WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('responses_id_seq', {id_num}, false);''')
    db.conn.commit()

    cursor.execute('''SELECT last_value FROM requests_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM requests WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('requests_id_seq', {id_num}, false);''')
    db.conn.commit()


def test_get_request_count(db):
    cursor = db.conn.cursor()
    num = db.get_request_count()

    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""INSERT INTO requests(city,request_time) VALUES (%s,%s);""", (city_name, request_time))
    db.conn.commit()

    assert db.get_request_count() == 1 + num

    cursor.execute('''SELECT last_value FROM requests_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM requests WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('requests_id_seq', {id_num}, false);''')
    db.conn.commit()


def test_get_successful_request_count(db):
    cursor = db.conn.cursor()
    num = db.get_successful_request_count()

    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""INSERT INTO requests(city,request_time) VALUES (%s,%s);""", (city_name, request_time))
    db.conn.commit()

    city_name = "rasht"
    temperature = 30
    feels_like_temperature = 28.4
    last_update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = {'temperature': temperature, 'feels_like': feels_like_temperature, 'last_updated': last_update_time}

    cursor.execute(f'''INSERT INTO responses(request_id,city,temperature,feels_like_temperature,last_updated_time)
        VALUES (
        (SELECT last_value FROM requests_id_seq),
        '{city_name}',
        {weather_info['temperature']},
        {weather_info['feels_like']},
        '{weather_info['last_updated']}');''')
    db.conn.commit()

    assert db.get_successful_request_count() == 1 + num
    cursor.execute('''SELECT last_value FROM responses_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM responses WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('responses_id_seq', {id_num}, false);''')
    db.conn.commit()

    cursor.execute('''SELECT last_value FROM requests_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM requests WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('requests_id_seq', {id_num}, false);''')
    db.conn.commit()


def test_get_last_hour_requests(db):
    cursor = db.conn.cursor()
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""INSERT INTO requests(city,request_time) VALUES (%s,%s);""", (city_name, request_time))
    db.conn.commit()

    lst = db.get_last_hour_requests()

    assert lst[-1] == (city_name, request_time)
    cursor.execute('''SELECT last_value FROM requests_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM requests WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('requests_id_seq', {id_num}, false);''')
    db.conn.commit()


def test_get_city_request_count(db):
    cursor = db.conn.cursor()
    city_name = "rasht"

    lst = db.get_city_request_count()
    f_count = 0
    for item in lst:
        if item[0] == city_name:
            f_count = item[1]

    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""INSERT INTO requests(city,request_time) VALUES (%s,%s);""", (city_name, request_time))
    db.conn.commit()

    lst = db.get_city_request_count()
    s_count = 1
    for item in lst:
        if item[0] == city_name:
            s_count = item[1]

    assert s_count == f_count + 1
    cursor.execute('''SELECT last_value FROM requests_id_seq''')
    id_num = cursor.fetchone()[0]
    cursor.execute(f'''DELETE FROM requests WHERE id = {id_num};''')
    cursor.execute(f'''SELECT setval('requests_id_seq', {id_num}, false);''')
    db.conn.commit()
