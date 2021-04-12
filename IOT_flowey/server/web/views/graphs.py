from ..forms.plant_type import PlantTypeForm
from ..models.plant_type import PlantTypeModel, db
from ..models.plant_data import PlantDataModel, db
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import OperationalError
import datetime


graphs_bp = Blueprint('graphs', __name__, url_prefix='/graphs')


@graphs_bp.route('/')
def list_all():
    try:
        plants = PlantDataModel.query.with_entities(PlantDataModel.plant_id).distinct().all()
        print("HEREEEEEEE")
        print(plants)
    except OperationalError:
        plants = None

    return render_template('graphs/list.html',
                           plants=plants)


@graphs_bp.route('/<plant_id>')
def details(plant_id):
    labels = []
    values = []
    title = 'Measurements of plant id:' + plant_id
    plant_measurements = PlantDataModel.query.filter_by(plant_id=plant_id).all()
    for item in plant_measurements:
        labels.append(item.creation_date)
        values.append(item.humidity_1)
        type_id=item.plant_type_id

    plant_type = PlantTypeModel.query.filter_by(id=type_id).first()
    plant_type.humidity_min = 1230
    plant_type.humidity_max = 1240
    print (plant_type)

    return render_template('graphs/test2.html',
                           values=values,
                           labels=labels,
                           title=title,
                           plant_type=plant_type)


@graphs_bp.route('/test')
def test():
    legend = 'Monthly Data'

    labels = []
    values = []
    plant_measurements = PlantDataModel.query.filter_by(plant_id='fffa776abc9f47568e943904ce792d4b').all()
    for item in plant_measurements:
        #labels.append(item. creation_date.strftime("%d/%m - %H:%M"))
        labels.append(item.creation_date)
        values.append(item.humidity_1)
    #labels.append(datetime.datetime(2020, 8, 13, 23, 40, 11, 99399))
    #values.append(1234.1)
    labels.append(datetime.datetime(2021, 3, 13, 23, 50, 20, 99399))
    values.append(1234.1)
    labels.append(datetime.datetime(2021, 3, 13, 23, 50, 40, 99399))
    values.append(1234.0)
    return render_template('graphs/test.html',
                           values=values,
                           labels=labels,
                           legend=legend)

