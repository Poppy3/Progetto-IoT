from flask import Flask
from .views.homepage import homepage_bp
from .views.plant_type import plant_type_bp
from .views.graphs import graphs_bp
from .views.telegram_bot import telegram_bot_bp
# from .views.dev import dev_bp
from .extensions.json_encoder import DateTimeJSONEncoder
from .extensions.restful import api
from .extensions.sqlalchemy import db
from .extensions.scheduler import scheduler
from .models.plant_type import PlantTypeModel
from .models.plant_data import PlantDataModel
from .resources.plant_data import PlantDataAPI, PlantDataListAPI
from .resources.plant_type import PlantTypeAPI, PlantTypeListAPI
from .tasks import prediction
from .utils import randint, shrink_id, human_readable_time, get_random_color


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    print(f'\n!!! ATTENTION !!!\nusing SQLALCHEMY_DATABASE_URI = {app.config["SQLALCHEMY_DATABASE_URI"]}\n')

    app.json_encoder = DateTimeJSONEncoder

    # initialize extensions
    db.init_app(app)
    api.init_app(app)
    scheduler.init_app(app)
    # bot.init_app(app)

    with app.app_context():
        # creating db
        db.create_all()

        # register blueprints
        app.register_blueprint(homepage_bp)
        app.register_blueprint(plant_type_bp)
        app.register_blueprint(graphs_bp)
        app.register_blueprint(telegram_bot_bp)
        # app.register_blueprint(dev_bp)

        # register Api resource routing here
        api.add_resource(PlantDataAPI, '/plant_data/<int:plant_data_id>')
        api.add_resource(PlantDataListAPI, '/plant_data')
        api.add_resource(PlantTypeAPI, '/plant_type/<int:plant_type_id>', '/plant_type/<string:plant_type_name>')
        api.add_resource(PlantTypeListAPI, '/plant_type')

        # TODO vedi se usare scheduler
        # scheduler.start()

    @app.context_processor
    def utility_randint():
        """
        inserisce automagicamente una chiave 'randint'
        nel dictionary context di ogni render_template
        """
        return dict(randint=randint)

    @app.context_processor
    def utility_shrink_id():
        """
        inserisce automagicamente una chiave 'shrink_id'
        nel dictionary context di ogni render_template
        """
        return dict(shrink_id=shrink_id)

    @app.context_processor
    def utility_human_readable_time():
        """
            inserisce automagicamente una chiave 'human_readable_time'
            nel dictionary context di ogni render_template
        """
        return dict(human_readable_time=human_readable_time)

    @app.context_processor
    def utility_get_random_color():
        """
            inserisce automagicamente una chiave 'get_random_color'
            nel dictionary context di ogni render_template
        """
        return dict(get_random_color=get_random_color)

    return app
