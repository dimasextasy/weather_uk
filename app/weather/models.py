from app import db

from datetime import datetime


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    weathers = db.relationship('Weather', backref='city', lazy='dynamic')

    def __repr__(self):
        return '<City: {}>'.format(self.name)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_weather = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return '<Weather: {} {}>'.format(self.city, self.timestamp.strftime('%a %d %b %Y %H:%M'))
