import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_ECHO = True
    OPENWEATHERMAP_URL = 'http://api.openweathermap.org/data/2.5/weather?q={0}&appid=332aff71953e43412a946ab10190bc7a'
    cities_to_save_scheduler = ['London', 'New York']
