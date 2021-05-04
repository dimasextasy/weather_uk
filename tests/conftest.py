import json
from os.path import join

import pytest

from app import create_app, db
from config import basedir, Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SCHEDULER_API_ENABLED = False


@pytest.fixture()
def get_app():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    print('create db')
    yield app, db
    db.session.remove()
    db.drop_all()
    app_context.pop()
    print('drop db')


@pytest.fixture(scope='module')
def get_test_weather_response_json():
    print(basedir)
    with open(join(basedir, 'test/test_data/weather.response'), 'r') as file:
        response_text = file.read()
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        assert False, "Something wrong with weather.response test data"