from flask import jsonify
from flask_restful import Resource


class PlantData(Resource):
    def get(self, plant_data_id=None):
        if(plant_data_id is None):
            # accessing PlantData as a whole
            # TODO prendi i dati dal db MODEL e restituisci la lista
            return 'qui riceveresti la lista di PlantData'
        else:
            # accessing a specific PlantData
            # TODO prendi i dati dal db MODEL e restituisci quello desiderato
            plant_data = {'myKey': 'myValue',
                          'plant_id': plant_data_id,
                          'message': 'qui riceveresti i dati della PlantData voluta, se esiste'}
            return jsonify(plant_data)

    # TODO il resto
    # def post()
    # def delete()
