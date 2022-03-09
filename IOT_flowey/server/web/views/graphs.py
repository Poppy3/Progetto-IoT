from ..models.plant_type import PlantTypeModel, db
from ..models.plant_data import PlantDataModel, db
from flask import Blueprint, render_template
from pathlib import Path
from sqlalchemy.exc import OperationalError
import json


graphs_bp = Blueprint('graphs', __name__, url_prefix='/graphs')


@graphs_bp.route('/')
def list_all():
    try:
        plants = PlantDataModel.query.with_entities(PlantDataModel.plant_id).distinct().all()
    except OperationalError:
        plants = None

    return render_template('graphs/list.html',
                           title='Graphs',
                           plants=plants)


@graphs_bp.route('/id/<plant_id>')
def details(plant_id):
    try:
        plant_measurements = PlantDataModel.query.filter_by(plant_id=plant_id).order_by(PlantDataModel.creation_date).all()
    except OperationalError:
        plant_measurements = None
    labels = []
    data = []
    for i in range(10):
        data.append([])
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
        """ median works best for three values, it's more robust to errors """
        # humidity_mean = (item.humidity_1 + plant_item.humidity_2 + item.humidity_3) / 3
        humidity_median = sorted([item.humidity_1, item.humidity_2, item.humidity_3])[1]
        data[8].append(humidity_median)  # humidity average
        data[9].append((item.luminosity_1 + item.luminosity_2) / 2)  # luminosity average

    plant_info = plant_measurements[0]

    type_id = plant_measurements[0].plant_type_id
    try:
        plant_type = PlantTypeModel.query.filter_by(id=type_id).first()
    except OperationalError:
        plant_type = None

    plant_type.humidity_max = 70.0
    plant_type.humidity_min = 30.0

    return render_template('graphs/details.html',
                           values=data,
                           labels=labels,
                           title=f'Measurements of {plant_type.name}',
                           plant_type=plant_type,
                           plant_info=plant_info)


@graphs_bp.route('/humidity')
def humidity_graph():
    try:
        plant_measurements = PlantDataModel.query.order_by(PlantDataModel.creation_date).all()
    except OperationalError:
        plant_measurements = None
    try:
        plants_count = PlantDataModel.query.with_entities(PlantDataModel.plant_id).distinct().count()
    except OperationalError:
        plants_count = None

    labels = []
    data = []
    plants = PlantDataModel.query.group_by(PlantDataModel.plant_id).all()

    for item in plants:
        data.append([item.plant_id, item.gateway_id, item.bridge_id, [], []])  # last 2 are dht and median

    for plant_item in plant_measurements:
        labels.append(plant_item.creation_date)
        for data_item in data:
            if data_item[0] == plant_item.plant_id:
                data_item[3].append(plant_item.dht_humidity)
                """ median works best for three values, it's more robust to errors """
                # humidity_mean = (plant_item.humidity_1 + plant_item.humidity_2 + plant_item.humidity_3) / 3
                humidity_median = sorted([plant_item.humidity_1, plant_item.humidity_2, plant_item.humidity_3])[1]
                data_item[4].append(humidity_median)
            else:
                data_item[3].append('null')
                data_item[4].append('null')

    return render_template('graphs/single_measurement.html',
                           title='Humidity',
                           labels=labels,
                           data=data,
                           measure="Humidity")


@graphs_bp.route('/temperature')
def temperature_graph():
    try:
        plant_measurements = PlantDataModel.query.order_by(PlantDataModel.creation_date).all()
    except OperationalError:
        plant_measurements = None

    labels = []
    data = []
    plants = PlantDataModel.query.group_by(PlantDataModel.plant_id).all()

    for item in plants:
        data.append([item.plant_id, item.gateway_id, item.bridge_id, [], []])  # last 2 are dht temp, and normal temp

    for plant_item in plant_measurements:
        labels.append(plant_item.creation_date)
        for data_item in data:
            if data_item[0] == plant_item.plant_id:
                data_item[3].append(plant_item.dht_temperature)
                data_item[4].append(plant_item.temperature)
            else:
                data_item[3].append('null')
                data_item[4].append('null')

    return render_template('graphs/single_measurement.html',
                           title='Temperature',
                           labels=labels,
                           data=data,
                           measure="Temperature")


@graphs_bp.route('/luminosity')
def luminosity_graph():
    try:
        plant_measurements = PlantDataModel.query.order_by(PlantDataModel.creation_date).all()
    except OperationalError:
        plant_measurements = None

    labels = []
    data = []
    plants = PlantDataModel.query.group_by(PlantDataModel.plant_id).all()

    for item in plants:
        data.append([item.plant_id, item.gateway_id, item.bridge_id, []])  # last is luminosity mean

    for plant_item in plant_measurements:
        labels.append(plant_item.creation_date)
        for data_item in data:
            if data_item[0] == plant_item.plant_id:
                data_item[3].append((plant_item.luminosity_1 + plant_item.luminosity_2) / 2)
            else:
                data_item[3].append('null')

    return render_template('graphs/single_measurement.html',
                           title='Luminosity',
                           labels=labels,
                           data=data,
                           measure="Luminosity")


# ----- json functions to work with a local json file stored in the views folder

@graphs_bp.route('/json/<plant_id>')
def details_json(plant_id):
    p = Path(__file__).with_name('plant_data.json')

    with p.open('r') as f:
        plant_measurements = json.load(f)
        plant_measurements.sort(key=lambda x: x['creation_date'])
        labels = []
        data = []
        print(plant_measurements)
        for i in range(10):
            data.append([])
        title = 'Measurements of plant id:' + plant_id
        for item in plant_measurements:
            print(item)
            labels.append(item["creation_date"])
            data[0].append(item["dht_humidity"])
            data[1].append(item["dht_temperature"])
            data[2].append(item["humidity_1"])
            data[3].append(item["humidity_2"])
            data[4].append(item["humidity_3"])
            data[5].append(item["luminosity_1"])
            data[6].append(item["luminosity_2"])
            data[7].append(item["temperature"])
            data[8].append((item["humidity_1"]+item["humidity_2"]+item["humidity_3"])/3)  # humidity average
            data[9].append((item["luminosity_1"]+item["luminosity_2"])/2)  # luminosity average

        plant_info = plant_measurements[0]

        type_id = plant_measurements[0]["plant_type_id"]
        try:
            plant_type = PlantTypeModel.query.filter_by(id=type_id).first()
        except OperationalError:
            plant_type = None

        # plant_type.humidity_max = 70.0
        # plant_type.humidity_min = 30.0

        return render_template('graphs/details.html',
                               values=data,
                               labels=labels,
                               title=title,
                               plant_type=plant_type,
                               plant_info=plant_info)


@graphs_bp.route('/json/humidity')
def humidity_graph_json():
    p = Path(__file__).with_name('plant_data.json')

    with p.open('r') as f:
        plant_measurements = json.load(f)

    data = []
    labels = []
    plant_measurements.sort(key=lambda x: x['creation_date'])
    data.append(["43c311e2279f4dd2afce8bbcff62371d", "ARDUINO001", "RASPBERRY001", [], []])  # last 2 are dht and mean
    data.append(["c5a3b03d82944886bb1fdb30612d5c5d", "ARDUINO001", "RASPBERRY001", [], []])  # last 2 are dht and mean

    for plant_item in plant_measurements:
        labels.append(plant_item["creation_date"])
        for data_item in data:
            if data_item[0] == plant_item["plant_id"]:
                data_item[3].append(plant_item["dht_humidity"])
                data_item[4].append((plant_item["humidity_1"] + plant_item["humidity_2"] + plant_item["humidity_3"])/3)
            else:
                data_item[3].append('null')
                data_item[4].append('null')

    return render_template('graphs/single_measurement.html',
                           labels=labels,
                           data=data,
                           measure="Humidity")


@graphs_bp.route('/json/temperature')
def temperature_graph_json():
    p = Path(__file__).with_name('plant_data.json')

    with p.open('r') as f:
        plant_measurements = json.load(f)

    data = []
    labels = []
    plant_measurements.sort(key=lambda x: x['creation_date'])
    data.append(["43c311e2279f4dd2afce8bbcff62371d", "ARDUINO001", "RASPBERRY001", [], []])  # last 2 are dht and mean
    data.append(["c5a3b03d82944886bb1fdb30612d5c5d", "ARDUINO001", "RASPBERRY001", [], []])  # last 2 are dht and mean

    for plant_item in plant_measurements:
        labels.append(plant_item["creation_date"])
        for data_item in data:
            if data_item[0] == plant_item["plant_id"]:
                data_item[3].append(plant_item["dht_temperature"])
                data_item[4].append(plant_item["temperature"])
            else:
                data_item[3].append('null')
                data_item[4].append('null')

    return render_template('graphs/single_measurement.html',
                           labels=labels,
                           data=data,
                           measure="Temperature")


@graphs_bp.route('/json/luminosity')
def luminosity_graph_json():
    p = Path(__file__).with_name('plant_data.json')

    with p.open('r') as f:
        plant_measurements = json.load(f)

    data = []
    labels = []
    plant_measurements.sort(key=lambda x: x['creation_date'])
    data.append(["43c311e2279f4dd2afce8bbcff62371d", "ARDUINO001", "RASPBERRY001", []])
    data.append(["c5a3b03d82944886bb1fdb30612d5c5d", "ARDUINO001", "RASPBERRY001", []])

    for plant_item in plant_measurements:
        labels.append(plant_item["creation_date"])
        for data_item in data:
            if data_item[0] == plant_item["plant_id"]:
                data_item[3].append((plant_item["luminosity_1"] + plant_item["luminosity_2"])/2)
            else:
                data_item[3].append('null')

    return render_template('graphs/single_measurement.html',
                           labels=labels,
                           data=data,
                           measure="Luminosity")
