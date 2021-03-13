from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextField, FloatField


class PlantTypeForm(FlaskForm):
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