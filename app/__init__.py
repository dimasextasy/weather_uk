from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_apscheduler import APScheduler


db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.weather import bp as weather_bp
    app.register_blueprint(weather_bp, url_prefix='/weather')

    scheduler.init_app(app)
    from . import tasks
    if app.config['SCHEDULER_API_ENABLED']:
        scheduler.start()

    return app
