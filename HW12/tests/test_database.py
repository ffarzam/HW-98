import pytest
from HW12.database import WeatherDatabase


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
