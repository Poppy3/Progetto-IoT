from ..models.plant_type import PlantTypeModel, db
from ..models.plant_data import PlantDataModel, db
from flask import Blueprint, render_template
from sqlalchemy.exc import OperationalError

graphs_bp = Blueprint('graphs', __name__, url_prefix='/graphs')

@graphs_bp.route('/')
def list_all():
    try:
        plants = PlantDataModel.query.with_entities(PlantDataModel.plant_id).distinct().all()
    except OperationalError:
        plants = None

    return render_template('graphs/list.html',
                           plants=plants)


@graphs_bp.route('/<plant_id>')
def details(plant_id):
    try:
        plant_measurements = PlantDataModel.query.filter_by(plant_id=plant_id).all()
    except OperationalError:
        plant_measurements = None
    labels = []
    data = []
    for i in range(8):
        data.append([])
    title = 'Measurements of plant id:' + plant_id
    for item in plant_measurements:
        labels.append(item.creation_date)
        data[0].append(item.dht_humidity)
        data[1].append(item.dht_temperature)
        data[2].append(item.humidity_1)
        data[3].append(item.humidity_2)
        data[4].append(item.humidity_3)
        data[5].append(item.luminosity_1)
        data[6].append(item.luminosity_2)
        data[7].append(item.temperature)

    plant_info = plant_measurements[0]

    type_id = plant_measurements[0].plant_type_id
    try:
        plant_type = PlantTypeModel.query.filter_by(id=type_id).first()
    except OperationalError:
        plant_type = None

    #plant_type.humidity_max=70.0
    #plant_type.humidity_min=30.0

    return render_template('graphs/details.html',
                           values=data,
                           labels=labels,
                           title=title,
                           plant_type=plant_type,
                           plant_info = plant_info)

