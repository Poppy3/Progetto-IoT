from ..models.plant_data import PlantDataModel, db
from ..models.plant_type import PlantTypeModel
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, inputs


def base_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('plant_id', type=str)
    parser.add_argument('plant_type_name', type=str)
    parser.add_argument('bridge_id', type=str)
    parser.add_argument('gateway_id', type=str)
    parser.add_argument('creation_date', type=inputs.datetime_from_iso8601,
                        help='Expecting an ISO8601 formatted datetime')
    parser.add_argument('timestamp', type=inputs.positive)
    parser.add_argument('dht_humidity', type=float)
    parser.add_argument('dht_temperature', type=float)
    parser.add_argument('luminosity_1', type=int)
    parser.add_argument('luminosity_2', type=int)
    parser.add_argument('humidity_1', type=int)
    parser.add_argument('humidity_2', type=int)
    parser.add_argument('humidity_3', type=int)
    parser.add_argument('temperature', type=float)
    return parser


def get_parser():
    parser = base_parser().copy()
    parser.replace_argument('plant_id', type=str, nullable=False)
    parser.replace_argument('bridge_id', type=str, nullable=False)
    return parser


def post_parser():
    parser = base_parser().copy()
    parser.replace_argument('plant_id', type=str, required=True, nullable=False)
    parser.replace_argument('plant_type_name', type=str, required=True, nullable=False)
    parser.replace_argument('bridge_id', type=str, required=True, nullable=False)
    parser.replace_argument('gateway_id', type=str, required=True, nullable=False)
    return parser


class PlantDataAPI(Resource):
    def get(self, plant_data_id=None):
        plant_data = None
        if plant_data_id is not None:
            plant_data = PlantDataModel.query.get_or_404(plant_data_id)
        return jsonify(plant_data)


class PlantDataListAPI(Resource):
    def get(self):
        args = get_parser().parse_args()
        filter_by = {}
        if args.plant_id is not None:
            filter_by['plant_id'] = args.plant_id
        if args.bridge_id is not None:
            filter_by['bridge_id'] = args.bridge_id
        plant_datas = PlantDataModel.query.filter_by(**filter_by).all()
        return jsonify(plant_datas)

    def post(self):
        args = post_parser().parse_args()
        plant_type = PlantTypeModel.query.filter_by(name=args.plant_type_name).first_or_404()
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
        return make_response(jsonify(plant_data), 201)  # 201 - Created
