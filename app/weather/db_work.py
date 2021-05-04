from datetime import timedelta

from app import scheduler, db
from app.weather.models import Weather, City
from app.weather.services import WeatherData, _make_weather_string
from utils.error_handlers import InvalidUsage


def save_weather_to_db(weather_data):
    with scheduler.app.app_context():
        city_obj = City.query.filter_by(name=weather_data.city).first()
        if not city_obj:
            city_obj = City(name=weather_data.city)
            db.session.add(city_obj)
        weather_obj = Weather.query.filter_by(city=city_obj, timestamp=weather_data.weather_datetime).first()
        if not weather_obj:
            weather_obj = Weather(
                type_of_weather=weather_data.weather,
                temperature=weather_data.temperature,
                timestamp=weather_data.weather_datetime,
                city=city_obj
            )
            db.session.add(weather_obj)
        db.session.commit()


def get_weather_from_db(city_name, unit, weather_date=None):
    if weather_date:
        weather_object = db.session.query(Weather, City.name).\
            join(City, Weather.city_id == City.id).\
            filter(City.name == city_name).\
            filter(Weather.timestamp >= weather_date).\
            filter(Weather.timestamp < weather_date + timedelta(days=1)).\
            order_by(Weather.timestamp.desc()).first()
    else:
        weather_object = db.session.query(Weather, City.name). \
            join(City, Weather.city_id == City.id). \
            filter(City.name == city_name). \
            order_by(Weather.timestamp.desc()).first()
    if not weather_object:
        raise InvalidUsage('Not found a weather for the specific date or city', status_code=404)
    w_data = WeatherData(city=weather_object[1],
                         weather=weather_object[0].type_of_weather,
                         weather_datetime=weather_object[0].timestamp,
                         temperature=weather_object[0].temperature
                         )
    weather_string = _make_weather_string(w_data, unit)
    return weather_string
