from flask import Flask, Blueprint
from .views.test_view import main
from .extensions.restful import api
from .extensions.sqlalchemy import db
from .models.plant_type import PlantType as ModelPlantType
from .models.plant_data import PlantData as ModelPlantData
from .resources.plant_data import PlantData as ResourcePlantType


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    print(f'SQLALCHEMY_DATABASE_URI = {app.config["SQLALCHEMY_DATABASE_URI"]}')

    # initialize database extension
    db.init_app(app)

    # register Api resource routing here
    api.add_resource(ResourcePlantType, '/plants/<string:plant_data_id>')

    # initialize rest api extension
    api.init_app(app)

    # create db
    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(main)
    # todo resto

    return app
