from ..models.plant_data import PlantDataModel, db
from ..models.plant_type import PlantTypeModel
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, inputs

post_parser = reqparse.RequestParser()
post_parser.add_argument("plant_id", type=str, required=True, nullable=False)
post_parser.add_argument("plant_type_name", type=str, required=True, nullable=False)
post_parser.add_argument("bridge_id", type=str, required=True, nullable=False)
post_parser.add_argument("gateway_id", type=str, required=True, nullable=False)
post_parser.add_argument("creation_date", type=inputs.datetime_from_iso8601,
                         help='Expecting an ISO8601 formatted datetime')
post_parser.add_argument("timestamp", type=inputs.positive)
post_parser.add_argument("dht_humidity", type=float)
post_parser.add_argument("dht_temperature", type=float)
post_parser.add_argument("luminosity_1", type=int)
post_parser.add_argument("luminosity_2", type=int)
post_parser.add_argument("humidity_1", type=int)
post_parser.add_argument("humidity_2", type=int)
post_parser.add_argument("humidity_3", type=int)
post_parser.add_argument("temperature", type=float)


class PlantDataAPI(Resource):
    def get(self, plant_data_id=None):
        # TODO prendi i dati dal db MODEL e restituisci quello desiderato
        plant_data = {'TODO': 'TODO',
                      'plant_id': plant_data_id,
                      'message': 'TODO - qui riceveresti i dati della PlantData voluta, se esiste'}
        return jsonify(plant_data)


class PlantDataListAPI(Resource):
    def get(self):
        # TODO prendi i dati dal db MODEL e restituisci la lista
        return f'TODO - qui riceveresti la lista di PlantData'

    def post(self):
        args = post_parser.parse_args()
        plant_type = PlantTypeModel.query.filter_by(name=args.plant_type_name).first()
        if plant_type is None:
            status_code = 404
            message = f'No plant_type registered with the given "plant_type_name" = {args.plant_type_name}'
            return make_response(jsonify({'status_code':status_code, 'message': message}), status_code)

        plant_data = PlantDataModel(plant_id=args.plant_id,
                                    plant_type_id=plant_type.id,
                                    bridge_id=args.bridge_id,
                                    gateway_id=args.gateway_id,
                                    creation_date=args.creation_date,
                                    timestamp=args.timestamp,
                                    dht_humidity=args.dht_humidity,
                                    dht_temperature=args.dht_temperature,
                                    luminosity_1=args.luminosity_1,
                                    luminosity_2=args.luminosity_2,
                                    humidity_1=args.humidity_1,
                                    humidity_2=args.humidity_2,
                                    humidity_3=args.humidity_3,
                                    temperature=args.temperature)
        db.session.add(plant_data)
        db.session.commit()
        return jsonify({'id': plant_data.id})
