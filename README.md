# Install and Run
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

flask db upgrade
export FLASK_APP=weather_app.py
flask run

# Scheduled tasks
Scheduled tasks are in the app/tasks.py
Configuration of scheduled tasks are in the config.py

#