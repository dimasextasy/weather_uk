from datetime import datetime
from unittest.mock import patch

import pytest

from app.weather.services import WeatherData
from utils.error_handlers import InvalidUsage


@pytest.fixture(
    params=[
        ((300, 'K'), '300K'),
        ((300, 'C'), '27C'),
        ((300, 'F'), '80F'),
    ],
    ids=[
        'translate_kelvin',
        'translate_celsius',
        'translate_fahrenheit'
    ]
)
def translate_temperature_test_cases(request):
    return request.param


def test__convert_temperature_unit(translate_temperature_test_cases):
    from app.weather.services import _convert_temperature_unit
    result = _convert_temperature_unit(*translate_temperature_test_cases[0])
    assert result == translate_temperature_test_cases[1]


def test__make_weather_string():
    from app.weather.services import _make_weather_string
    from app.weather.services import WeatherData
    w_data = WeatherData(city='London',
                         weather='heavy rain',
                         weather_datetime=datetime(year=2021, month=4, day=28, hour=14, minute=20),
                         temperature=300
                         )
    result = _make_weather_string(weather_data=w_data, temp_unit='C')
    expected = 'London, Wed 28 Apr 2021 14:20, heavy rain, 27C'
    assert result == expected


def test__get_info_from_json(get_test_weather_response_json):
    from app.weather.services import _get_info_from_json
    result = _get_info_from_json(get_test_weather_response_json)
    expected = WeatherData(
        city='London',
        weather='haze',
        weather_datetime=datetime(2016, 12, 14, 15, 50, tzinfo=datetime.now().astimezone().tzinfo),
        temperature=284.07
    )
    assert result == expected


def test__get_info_from_json_fail():
    from app.weather.services import _get_info_from_json
    pytest.raises(InvalidUsage, _get_info_from_json, {'error': 'Not found'})


def test_get_weather_string_from_api(get_test_weather_response_json):
    from app.weather.services import get_weather_string_from_api
    expected = 'London, Wed 14 Dec 2016 15:50, haze, 52F'
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = get_test_weather_response_json
        result = get_weather_string_from_api('London', 'F')
    assert result == expected


def test_get_weather_from_api(get_test_weather_response_json):
    from app.weather.services import get_weather_from_api
    expected = WeatherData(
        city='London',
        weather='haze',
        weather_datetime=datetime(2016, 12, 14, 15, 50, tzinfo=datetime.now().astimezone().tzinfo),
        temperature=284.07
    )
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = get_test_weather_response_json
        result = get_weather_from_api('London')
    assert result == expected
