from config import Config
from app import scheduler
from app.weather.db_work import save_weather_to_db
from app.weather.services import get_weather_from_api


@scheduler.task('interval', id='save_weather_job', seconds=600)
def save_weather_to_db_task():
    for city in Config.cities_to_save_scheduler:
        weather = get_weather_from_api(city)
        save_weather_to_db(weather)
