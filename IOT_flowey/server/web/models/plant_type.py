from ..extensions.sqlalchemy import db
from sqlalchemy.orm import validates
import datetime


class PlantTypeModel(db.Model):
    __tablename__ = 'plant_type'

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

    plant_data = db.relationship('PlantDataModel', backref='plant_type', lazy=True)

    #@validates('name')
    #def convert_lower(self, key, value):
    #    return value.lower()
