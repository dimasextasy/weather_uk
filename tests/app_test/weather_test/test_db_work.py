from datetime import datetime, date

import pytest

from app.weather.models import Weather, City
from app.weather.services import WeatherData
from utils.error_handlers import InvalidUsage


def test_save_weather_to_db(get_app):
    from app.weather.db_work import save_weather_to_db
    local_db = get_app[1]
    w_data = WeatherData(city='London',
                         weather='heavy rain',
                         weather_datetime=datetime(year=2021, month=4, day=28, hour=14, minute=20),
                         temperature=300
                         )
    save_weather_to_db(w_data)
    result_row = local_db.session.query(Weather).all()
    assert len(result_row) == 1
    assert result_row[0].type_of_weather == 'heavy rain'
    assert result_row[0].timestamp == datetime(year=2021, month=4, day=28, hour=14, minute=20)


def test_get_last_weather_from_db(get_app):
    from app.weather.db_work import get_weather_from_db
    local_db = get_app[1]
    city_obj = City(name='London')
    local_db.session.add(city_obj)
    for index in range(5):
        weather = Weather(
            type_of_weather='heavy rain',
            timestamp=datetime(year=2021, month=4, day=28, hour=14 + index, minute=20),
            temperature=300,
            city=city_obj
        )
        local_db.session.add(weather)
    local_db.session.commit()
    result = get_weather_from_db(city_name='London', unit='C')
    assert result == 'London, Wed 28 Apr 2021 18:20, heavy rain, 27C'


def test_get_last_weather_from_db_no_data(get_app):
    from app.weather.db_work import get_weather_from_db
    local_db = get_app[1]
    city_obj = City(name='London')
    local_db.session.add(city_obj)
    local_db.session.commit()
    pytest.raises(InvalidUsage, get_weather_from_db, city_name='London', unit='C')


def test_get_weather_by_date_from_db(get_app):
    from app.weather.db_work import get_weather_from_db
    local_db = get_app[1]
    city_obj = City(name='London')
    local_db.session.add(city_obj)
    for index in range(3):
        weather = Weather(
            type_of_weather='heavy rain',
            timestamp=datetime(year=2021, month=4 + index, day=28, hour=14, minute=20),
            temperature=300,
            city=city_obj
        )
        local_db.session.add(weather)
    local_db.session.commit()
    result = get_weather_from_db('London', 'F', date(year=2021, month=6, day=28))
    assert result == 'London, Mon 28 Jun 2021 14:20, heavy rain, 80F'
