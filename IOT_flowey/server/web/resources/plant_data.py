from flask import jsonify
from flask_restful import Resource


class PlantData(Resource):
    def get(self, plant_data_id):
        plant_data = {}  # TODO rimuovere, è solo per non avere errori
        # TODO get plant_data from db
        return jsonify(plant_data)

    # TODO il resto
