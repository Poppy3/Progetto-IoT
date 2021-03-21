from flask import Flask, Blueprint
import random
from .views.test_view import main
from .views.plant_type import plant_type_bp
from .extensions.restful import api
from .extensions.sqlalchemy import db
from .models.plant_type import PlantTypeModel
from .models.plant_data import PlantDataModel
from .resources.plant_data import PlantDataAPI, PlantDataListAPI


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    print(f'\n!!! ATTENTION !!!\nusing SQLALCHEMY_DATABASE_URI = {app.config["SQLALCHEMY_DATABASE_URI"]}\n')

    # initialize database extension
    db.init_app(app)

    # register Api resource routing here
    api.add_resource(PlantDataAPI, '/plant_data/<string:plant_data_id>')
    api.add_resource(PlantDataListAPI, '/plant_data')

    # initialize rest api extension
    api.init_app(app)

    # create db
    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(main)
    app.register_blueprint(plant_type_bp)
    # todo resto


    # inserisce automagicamente una chiave 'randint'
    # nel dictionary context di ogni render_template
    @app.context_processor
    def utility_randint():
        def randint(a, b):
            return random.randint(a, b)

        return dict(randint=randint)

    return app
