import pytest
from HW12.database import WeatherDatabase


@pytest.fixture
def db():
    db = WeatherDatabase()
    yield db
    db.close()
