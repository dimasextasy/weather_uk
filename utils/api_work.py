from utils.error_handlers import InvalidUsage, APIUnavailableError
from json import JSONDecodeError
import time
import requests


def get_external_api_response(url, retry_count=0):
    try:
        if retry_count > 2:
            raise APIUnavailableError('Timeout error! Server does not respond.')
        response = requests.get(url, timeout=3)
        response_json = response.json()
        if response.ok:
            return response_json
        else:
            raise InvalidUsage('The external API return non-ok status', status_code=400, payload=response_json)
    except requests.exceptions.Timeout:
        # Sleep and retry to get API 3 times
        time.sleep(1)
        return get_external_api_response(url, retry_count + 1)
    except requests.exceptions.ConnectionError:
        raise APIUnavailableError('Timeout error! Server does not respond.')
    except JSONDecodeError:
        raise InvalidUsage('The API return non-json format', status_code=400)
