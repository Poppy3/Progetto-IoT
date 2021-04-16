from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class PlantTypeForm(FlaskForm):
    name = StringField('Name', description='Plant Name',
                       validators=[DataRequired(), Length(min=3, max=128)])
    description = TextAreaField('Description', description='Plant Description',
                                validators=[Length(max=5000), Optional()])
    humidity_min = DecimalField('Humidity Min', description='Minimum humidity that the plant should endure',
                                validators=[NumberRange(min=0, max=2000000000), Optional()])
    humidity_max = DecimalField('Humidity Max', description='Maximum humidity that the plant should endure',
                                validators=[NumberRange(min=0, max=2000000000), Optional()])
    humidity_tolerance_time = IntegerField('Tolerance Time',
                                           description='Maximum time (in seconds) allowed for the plant '
                                                       'should it endure adverse humidity levels',
                                           validators=[NumberRange(min=0, max=2000000000), Optional()])
    luminosity_min = DecimalField('Luminosity Min', description='Minimum luminosity that the plant should endure',
                                  validators=[NumberRange(min=0, max=2000000000), Optional()])
    luminosity_max = DecimalField('Luminosity Max', description='Maximum luminosity that the plant should endure',
                                  validators=[NumberRange(min=0, max=2000000000), Optional()])
    luminosity_tolerance_time = IntegerField('Tolerance Time',
                                             description='Maximum time (in seconds) allowed for the plant '
                                                         'should it endure adverse luminosity levels',
                                             validators=[NumberRange(min=0, max=2000000000), Optional()])
    temperature_min = DecimalField('Temperature Min',
                                   description='Minimum temperature (°C) that the plant should endure',
                                   validators=[NumberRange(min=-100, max=100), Optional()])
    temperature_max = DecimalField('TemperatureMax',
                                   description='Maximum temperature (°C) that the plant should endure',
                                   validators=[NumberRange(min=-100, max=100), Optional()])
    temperature_tolerance_time = IntegerField('Tolerance Time',
                                              description='Maximum time (in seconds) allowed for the plant '
                                                          'should it endure adverse temperature levels',
                                              validators=[NumberRange(min=0, max=2000000000), Optional()])
