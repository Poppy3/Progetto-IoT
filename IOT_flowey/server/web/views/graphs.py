from ..forms.plant_type import PlantTypeForm
from ..models.plant_type import PlantTypeModel, db
from ..models.plant_data import PlantDataModel, db
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import OperationalError


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
    plant_measurements = PlantDataModel.query.filter_by(plant_id=plant_id).all()
    print(plant_measurements)
    return render_template('graphs/details.html',
                           title=plant_id,
                           plant_data=plant_measurements)


@graphs_bp.route('/test')
def test():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('graphs/test2.html',
                           values=values,
                           labels=labels,
                           legend=legend)

