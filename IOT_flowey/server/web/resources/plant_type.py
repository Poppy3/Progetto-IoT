from ..models.plant_type import PlantTypeModel
from flask import jsonify
from flask_restful import Resource


class PlantTypeAPI(Resource):
    def get(self, plant_type_id=None, plant_type_name=None):
        plant_type = None
        if plant_type_id is not None:
            plant_type = PlantTypeModel.query.get_or_404(plant_type_id)
        elif plant_type_name is not None:
            plant_type = PlantTypeModel.query.filter_by(name=plant_type_name).first_or_404()
        return jsonify(plant_type)


class PlantTypeListAPI(Resource):
    def get(self):
        plant_types = PlantTypeModel.query.all()
        return jsonify(plant_types)
