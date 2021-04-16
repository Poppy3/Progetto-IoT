from ..extensions.sqlalchemy import db
from ..models.plant_data import PlantDataModel
from dataclasses import dataclass
from sqlalchemy.orm import validates
import datetime


@dataclass
class PlantTypeModel(db.Model):
    __tablename__ = 'plant_type'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_modified: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                                                 onupdate=datetime.datetime.utcnow)
    name: str = db.Column(db.String(length=128), nullable=False, unique=True)
    description: str = db.Column(db.Text)
    humidity_min: float = db.Column(db.Float)
    humidity_max: float = db.Column(db.Float)
    humidity_tolerance_time: int = db.Column(db.Integer)
    luminosity_min: float = db.Column(db.Float)
    luminosity_max: float = db.Column(db.Float)
    luminosity_tolerance_time: int = db.Column(db.Integer)
    temperature_min: float = db.Column(db.Float)
    temperature_max: float = db.Column(db.Float)
    temperature_tolerance_time: int = db.Column(db.Integer)

    plant_data = db.relationship('PlantDataModel',
                                 # backref='plant_type',
                                 lazy=True)

    # @validates('name')
    # def convert_lower(self, key, value):
    #     return value.lower()
