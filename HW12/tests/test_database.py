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
