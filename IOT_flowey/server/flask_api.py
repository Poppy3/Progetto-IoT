#local
#import gateway_connector.py

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)


PLANT_DB = {
    'plant1': {'data': {
        'media': 123.12,
        'gateway_UUID': "ARDUINO001",
        'timestamp': 1234,
        'dht_temperature': 12.34,
        'dht_humidity': 12.34,
        'temperature': 12.34,
        'luminosity_1': 1234,
        'luminosity_2': 1234,
        'humidity_1': 1234,
        'humidity_2': 1234,
        'humidity_3': 1234,
        'luminosity_avg': 123.12,
        'luminosity_delta': 0.123,
        'humidity_avg': 123.12,
        'Humidity_delta': 0.123,
        'type': 'cactus',
        'bridge_UUID': 'RASPBERRY001'
        }
    },
    'plant2': {'data': {
        'media': 124.12,
        'gateway_UUID': "ARDUINO001",
        'timestamp': 1234,
        'dht_temperature': 12.34,
        'dht_humidity': 12.34,
        'temperature': 12.34,
        'luminosity_1': 1234,
        'luminosity_2': 1234,
        'humidity_1': 1234,
        'humidity_2': 1234,
        'humidity_3': 1234,
        'luminosity_avg': 123.12,
        'luminosity_delta': 0.123,
        'humidity_avg': 123.12,
        'Humidity_delta': 0.123,
        'type': 'cactus',
        'bridge_UUID': 'RASPBERRY001'
        }
    }
}


def abort_if_plant_doesnt_exist(plant_id):
    if plant_id not in PLANT_DB:
        abort(404, message="Plant {} doesn't exist".format(plant_id))


parser = reqparse.RequestParser()
parser.add_argument('dataa')


# Lista delle piante
class PlantList(Resource):
    # Visualizza la lista di tutti i valori più recenti letti dal bridge
    def get(self):
        return PLANT_DB

    #aggiunge misurazioni di una pianta
    def post(self):
        args = parser.parse_args()
        plant_id = int(max(PLANT_DB.keys()).lstrip('plant')) + 1
        plant_id = 'plant%i' % plant_id
        print(plant_id)
        PLANT_DB[plant_id] = {'data': args['data']}
        print(PLANT_DB[plant_id])
        return PLANT_DB[plant_id], 201


# Single Plant
class Plant(Resource):
    def get(self, plant_id):
        abort_if_plant_doesnt_exist(plant_id)
        return PLANT_DB[plant_id]

    def delete(self, plant_id):
        abort_if_plant_doesnt_exist(plant_id)
        del PLANT_DB[plant_id]
        return '', 204


##
## Actually setup the Api resource routing here
##
api.add_resource(PlantList, '/plants')
api.add_resource(Plant, '/plants/<plant_id>')


if __name__ == '__main__':
    app.run(debug=True)
