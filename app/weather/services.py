from utils.api_work import get_external_api_response
from utils.error_handlers import InvalidUsage
from config import Config

from datetime import datetime
from collections import namedtuple

WeatherData = namedtuple('WeatherData', ['city', 'weather', 'weather_datetime', 'temperature'])


def get_weather_string_from_api(city, unit):
    weather_data = get_weather_from_api(city)
    weather_string = _make_weather_string(weather_data, unit)
    return weather_string


def get_weather_from_api(city):
    url = Config.OPENWEATHERMAP_URL.format(city)
    response_json = get_external_api_response(url)
    weather_data = _get_info_from_json(response_json)
    return weather_data


def _get_info_from_json(response_json):
    try:
        city = response_json['name']
        unix_time = datetime.fromtimestamp(response_json['dt'], datetime.now().astimezone().tzinfo)
        type_of_weather = response_json['weather'][0]['description']
        kelvin_temp = response_json['main']['temp']
        w_data = WeatherData(city=city, weather=type_of_weather, weather_datetime=unix_time, temperature=kelvin_temp)
        return w_data
    except KeyError:
        raise InvalidUsage('An error occurred while retrieving data from an external request.', status_code=404,
                           payload=response_json)


def _make_weather_string(weather_data, temp_unit):
    datetime_str = weather_data.weather_datetime.strftime('%a %d %b %Y %H:%M')
    temperature_str = _convert_temperature_unit(weather_data.temperature, temp_unit)
    return '{city}, {datetime_str}, {weather}, {temperature}'.format(
        city=weather_data.city,
        datetime_str=datetime_str,
        weather=weather_data.weather,
        temperature=temperature_str
    )


def _convert_temperature_unit(kelvin_temp, type_of_weather):
    conversion_table = {
        'K': '{}K'.format(kelvin_temp),
        'C': '{}C'.format(round(kelvin_temp - 273.15)),
        'F': '{}F'.format(round(9/5 * kelvin_temp - 459.67))
    }
    return conversion_table[type_of_weather]
