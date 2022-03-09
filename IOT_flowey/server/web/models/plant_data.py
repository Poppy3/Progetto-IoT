from ..extensions.sqlalchemy import db
from dataclasses import dataclass
from datetime import datetime


@dataclass()
class PlantDataModel(db.Model):
    __tablename__ = 'plant_data'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_modified: datetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    plant_id: str = db.Column(db.String(length=50), nullable=False)
    bridge_id: str = db.Column(db.String(length=50), nullable=False)
    gateway_id: str = db.Column(db.String(length=50), nullable=False)
    creation_date: datetime = db.Column(db.DateTime)
    timestamp: int = db.Column(db.BigInteger)
    dht_humidity: float = db.Column(db.Float)
    dht_temperature: float = db.Column(db.Float)
    luminosity_1: int = db.Column(db.Integer)
    luminosity_2: int = db.Column(db.Integer)
    humidity_1: int = db.Column(db.Integer)
    humidity_2: int = db.Column(db.Integer)
    humidity_3: int = db.Column(db.Integer)
    temperature: float = db.Column(db.Float)

    plant_type_id: int = db.Column(db.Integer, db.ForeignKey('plant_type.id'), nullable=False)
