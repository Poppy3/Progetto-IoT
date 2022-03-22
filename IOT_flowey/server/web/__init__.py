from flask import Flask

from .extensions import (
    DateTimeJSONEncoder,
    api,
    db,
    scheduler,
)
from .models import PlantTypeModel, PlantDataModel
from .resources.plant_data import PlantDataAPI, PlantDataListAPI
from .resources.plant_type import PlantTypeAPI, PlantTypeListAPI
from .tasks import prediction
from .utils import randint, shrink_id, human_readable_time, get_random_color
from .views import (
    # dev_bp
    homepage_bp,
    plant_type_bp,
    graphs_bp,
    telegram_bot_bp,
)


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.json_encoder = DateTimeJSONEncoder

    # initialize extensions
    db.init_app(app)
    api.init_app(app)
    scheduler.init_app(app)

    with app.app_context():
        # creating db
        db.create_all()

        # register blueprints
        # app.register_blueprint(dev_bp)
        app.register_blueprint(homepage_bp)
        app.register_blueprint(graphs_bp)
        app.register_blueprint(plant_type_bp)
        app.register_blueprint(telegram_bot_bp)

        # register Api resource routing here
        api.add_resource(PlantDataAPI, '/plant_data/<int:plant_data_id>')
        api.add_resource(PlantDataListAPI, '/plant_data')
        api.add_resource(PlantTypeAPI, '/plant_type/<int:plant_type_id>', '/plant_type/<string:plant_type_name>')
        api.add_resource(PlantTypeListAPI, '/plant_type')

        # scheduler.start()

    @app.context_processor
    def utility_randint():
        """inserts 'randint' into the context of rendered templates"""
        return dict(randint=randint)

    @app.context_processor
    def utility_shrink_id():
        """inserts 'shrink_id' into the context of rendered templates"""
        return dict(shrink_id=shrink_id)

    @app.context_processor
    def utility_human_readable_time():
        """inserts 'human_readable_time' into the context of rendered templates"""
        return dict(human_readable_time=human_readable_time)

    @app.context_processor
    def utility_get_random_color():
        """inserts 'get_random_color' into the context of rendered templates"""
        return dict(get_random_color=get_random_color)

    return app
