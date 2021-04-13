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

    return render_template('graphs/details.html',
                           values=values,
                           labels=labels,
                           title=title,
                           plant_type=plant_type)


@graphs_bp.route('/test')
def test():
    labels = []
    title = 'Measurements of plant id:'# + plant_id
    plant_measurements = PlantDataModel.query.filter_by(plant_id='442217262fbc447bbab8f677f4a50fd1').all()
    for item in plant_measurements:
        labels.append(item.creation_date)
        type_id=item.plant_type_id
    plant_type = PlantTypeModel.query.filter_by(id=type_id).first()

    return render_template('graphs/test2.html',
                           data=plant_measurements,
                           labels=labels,
                           plant_type=plant_type,
                           title=title)

