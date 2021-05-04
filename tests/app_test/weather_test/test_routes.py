from datetime import datetime
from unittest.mock import patch

import pytest
import requests

from app.weather.models import City, Weather


@pytest.fixture
def client(get_app):
    return get_app[0].test_client()


@pytest.fixture()
def create_one_weather_for_client(get_app):
    app, db = get_app
    city_obj = City(name='London')
    db.session.add(city_obj)
    weather = Weather(
        type_of_weather='heavy rain',
        timestamp=datetime(year=2021, month=4, day=28, hour=14, minute=20),
        temperature=300,
        city=city_obj
    )
    db.session.add(weather)
    db.session.commit()
    client = app.test_client()
    return client


def test_weather_page(client, get_test_weather_response_json):
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = get_test_weather_response_json
        response = client.get('/weather/London?unit=F')
    assert response.status_code == 200
    assert response.json == {'weather': 'London, Wed 14 Dec 2016 15:50, haze, 52F'}


def test_weather_page_unexpected_unit(client):
    response = client.get('/weather/London?unit=H')
    assert response.status_code == 400
    assert response.json == {'error_message': 'Wrong temperature unit character. Please use - F, C or K'}


def test_weather_page_api_timeout_empty_base(client):
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout
        response = client.get('/weather/London?unit=F')
    assert response.status_code == 404
    assert response.json == {'error_message': 'Not found a weather for the specific date or city'}


def test_weather_page_api_timeout_with_data(create_one_weather_for_client):
    client = create_one_weather_for_client
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout
        response = client.get('/weather/London?unit=F')
    assert response.status_code == 200
    assert response.json == {'weather': 'London, Wed 28 Apr 2021 14:20, heavy rain, 80F'}


def test_weather_page_by_date_with_data(create_one_weather_for_client):
    client = create_one_weather_for_client
    response = client.get('/weather/London/2021-04-28')
    assert response.status_code == 200
    assert response.json == {'weather': 'London, Wed 28 Apr 2021 14:20, heavy rain, 27C'}


def test_weather_page_by_date_without_data(client):
    response = client.get('/weather/London/2021-04-28')
    assert response.status_code == 404
    assert response.json == {'error_message': 'Not found a weather for the specific date or city'}