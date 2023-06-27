import pytest
from HW12.database import WeatherDatabase
import datetime


@pytest.fixture
def db():
    db = WeatherDatabase(dbname="test")
    yield db
    cursor = db.cur
    cursor.execute('''DROP TABLE IF EXISTS responses;''')
    cursor.execute('''DROP TABLE IF EXISTS requests;''')
    cursor.execute('''DROP TABLE IF EXISTS users;''')
    db.conn.commit()

    # cursor.execute('''SELECT last_value FROM responses_id_seq''')
    # id_num = cursor.fetchone()[0]
    # cursor.execute(f'''DELETE FROM responses WHERE id = {id_num};''')
    # cursor.execute(f'''SELECT setval('responses_id_seq', {id_num}, false);''')
    # db.conn.commit()
    #
    # cursor.execute('''SELECT last_value FROM requests_id_seq''')
    # id_num = cursor.fetchone()[0]
    # cursor.execute(f'''DELETE FROM requests WHERE id = {id_num};''')
    # cursor.execute(f'''SELECT setval('requests_id_seq', {id_num}, false);''')
    # db.conn.commit()

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


def test_set_user(db):
    db.create_tables()
    username = "ffarzam"
    password = "Ffarzam_1992"
    db.set_user(username, password)

    cursor = db.conn.cursor()
    cursor.execute("SELECT username FROM users;")
    row = cursor.fetchone()

    assert row[0] == username


def test_save_request_data(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.save_request_data(user_id, city_name, request_time)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM requests;")
    row = cursor.fetchone()

    assert row[1] == user_id
    assert row[2] == city_name
    assert row[3] == datetime.datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S")


def test_save_response_data(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    cursor = db.conn.cursor()
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time) 
                            VALUES ({user_id},'{city_name}', '{request_time}');""")
    city_name = "rasht"
    temperature = 30.5
    feels_like_temperature = 28.4
    last_update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = {'temperature': temperature, 'feels_like': feels_like_temperature, 'last_updated': last_update_time}

    db.save_response_data(city_name, weather_info)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM responses;")
    row = cursor.fetchone()

    assert row[2] == city_name
    assert float(row[3]) == temperature
    assert float(row[4]) == feels_like_temperature
    assert row[5] == datetime.datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")


def test_get_request_count(db):
    db.create_tables()

    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    cursor = db.conn.cursor()
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time) 
                                VALUES ({user_id},'{city_name}', '{request_time}');""")

    assert db.get_request_count() == 1


def test_get_successful_request_count(db):
    db.create_tables()

    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    cursor = db.conn.cursor()
    city_name = "invalid"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time) 
                                    VALUES ({user_id},'{city_name}', '{request_time}');""")
    db.conn.commit()

    username = "fffarzam"
    password = "Fffarzam_1992"
    db.set_user(username, password)
    user_id = 2
    city_name = "tehran"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time) 
                                        VALUES ({user_id},'{city_name}', '{request_time}');""")
    db.conn.commit()

    city_name = "tehran"
    temperature = 30.0
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

    assert db.get_successful_request_count() == 1


def test_get_last_hour_requests(db):
    db.create_tables()

    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 1
    city_name = "tehran"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time) 
                                            VALUES ({user_id},'{city_name}', '{request_time}');""")
    db.conn.commit()

    cursor = db.conn.cursor()
    username = "fffarzam"
    password = "Fffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    user_id = 2
    city_name1 = "rasht"
    request_time1 = "2023-04-08 23:11:11"
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time) 
                                                VALUES ({user_id},'{city_name1}', '{request_time1}');""")
    db.conn.commit()

    lst = db.get_last_hour_requests()

    assert lst[-1] == (city_name, request_time)
    assert len(lst) == 1


def test_get_city_request_count(db):
    db.create_tables()
    cursor = db.conn.cursor()
    username = "ffarzam"
    password = "Ffarzam_1992"
    cursor.execute(
        f"""INSERT INTO Users(username,password) VALUES ('{username}',crypt('{password}', gen_salt('bf')));""")
    db.conn.commit()

    f_count = 0

    user_id = 1
    city_name = "rasht"
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = db.conn.cursor()
    cursor.execute(f"""INSERT INTO requests(user_id,city,request_time) 
                                            VALUES ({user_id},'{city_name}', '{request_time}');""")
    db.conn.commit()
    lst = db.get_city_request_count()
    for item in lst:
        if item[0] == city_name:
            s_count = item[1]

    assert s_count == f_count + 1
