from web.extensions.sqlalchemy import db
import datetime


class PlantType(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    name = db.Column(db.String(length=128), nullable=False, unique=True)
    description = db.Column(db.Text)
    humidity_min = db.Column(db.Float)
    humidity_max = db.Column(db.Float)
    humidity_tolerance_time = db.Column(db.Integer)
    luminosity_min = db.Column(db.Float)
    luminosity_max = db.Column(db.Float)
    luminosity_tolerance_time = db.Column(db.Integer)
    temperature_min = db.Column(db.Float)
    temperature_max = db.Column(db.Float)
    temperature_tolerance_time = db.Column(db.Integer)

    plant_data = db.relationship('PlantData', backref='plant_type', lazy=True)
