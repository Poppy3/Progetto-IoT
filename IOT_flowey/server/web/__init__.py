from flask import Flask, Blueprint
from web.views.test_view import main
from web.extensions.restful import api
from web.extensions.sqlalchemy import db
from web.models.plant_type import PlantType as ModelPlantType
from web.models.plant_data import PlantData as ModelPlantData
from web.resources.plant_data import PlantData as ResourcePlantType


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    print(f'SQLALCHEMY_DATABASE_URI = {app.config["SQLALCHEMY_DATABASE_URI"]}')

    # initialize the extensions
    db.init_app(app)
    api.init_app(app)

    with app.app_context():
        db.create_all()

    # register Api resource routing here
    api.add_resource(ResourcePlantType, '/plants/<string:plant_data_id>')
    # TODO resto

    # register blueprints
    app.register_blueprint(main)
    # todo resto

    return app
