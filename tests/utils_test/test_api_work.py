from unittest.mock import patch


import pytest
import requests

from utils.error_handlers import APIUnavailableError


def test_get_external_api_response(get_test_weather_response_json):
    from utils.api_work import get_external_api_response
    from config import Config
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = get_test_weather_response_json
        url = Config.OPENWEATHERMAP_URL.format('London')
        result = get_external_api_response(url)
        assert result == get_test_weather_response_json


def test_get_external_api_response_retry():
    from utils.api_work import get_external_api_response
    from config import Config
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout
        url = Config.OPENWEATHERMAP_URL.format('London')
        pytest.raises(APIUnavailableError, get_external_api_response, url)
        assert mock_get.call_count == 3


def test_get_external_api_response_fail():
    from utils.api_work import get_external_api_response
    from config import Config
    from utils.error_handlers import InvalidUsage
    with patch('utils.api_work.requests.get') as mock_get:
        mock_get.return_value.ok = False
        mock_get.return_value.json.return_value = {'error': 'No data found'}
        url = Config.OPENWEATHERMAP_URL.format('London')
        pytest.raises(InvalidUsage, get_external_api_response, url)
