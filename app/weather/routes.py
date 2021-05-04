from datetime import datetime

from app.weather import bp
from app.weather.db_work import get_weather_from_db
from app.weather.services import get_weather_string_from_api
from utils.error_handlers import InvalidUsage, APIUnavailableError

from flask import request, jsonify, make_response


@bp.route('/<string:city>', methods=['GET'])
def get_weather(city):
    unit = request.args.get('unit', 'C')
    if unit not in ('K', 'F', 'C'):
        raise InvalidUsage('Wrong temperature unit character. Please use - F, C or K', status_code=400)
    try:
        response = get_weather_string_from_api(city, unit)
    except APIUnavailableError:
        response = get_weather_from_db(city, unit)
    return jsonify({'weather': response})


@bp.route('/<string:city>/<string:date_str>', methods=['GET'])
def get_specific_datetime_weather(city, date_str):
    try:
        unit = request.args.get('unit', 'C')
        if unit not in ('K', 'F', 'C'):
            raise InvalidUsage('Wrong temperature unit character. Please use - F, C or K', status_code=400)
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weather = get_weather_from_db(city, unit, datetime_obj)
        return jsonify({'weather': weather})
    except ValueError:
        raise InvalidUsage('Date format is not recognised. Please use the YYYY-MM-DD format', status_code=400)


@bp.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
