from ..extensions.sqlalchemy import db
import datetime


class PlantData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    plant_id = db.Column(db.String(length=50), nullable=False)
    device_id = db.Column(db.String(length=50), nullable=False)
    creation_date = db.Column(db.DateTime)
    timestamp = db.Column(db.BigInteger)
    dht_humidity = db.Column(db.Float)
    dht_temperature = db.Column(db.Float)
    luminosity_1 = db.Column(db.Integer)
    luminosity_2 = db.Column(db.Integer)
    humidity_1 = db.Column(db.Integer)
    humidity_2 = db.Column(db.Integer)
    humidity_3 = db.Column(db.Integer)
    temperature = db.Column(db.Float)

    plant_type_id = db.Column(db.Integer, db.ForeignKey('plant_type.id'), nullable=False)
