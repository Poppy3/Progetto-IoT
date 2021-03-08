################################################################################
# The Application Factory.
# Any configuration, registration, and other setup the application needs will
# happen inside the function, then the application will be returned.
# See: https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/
################################################################################


# local
from .. import config as cfg
from . import db

# standard libraries
from flask import Flask
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=cfg.FLASK.INSTANCE_RELATIVE_CONFIG,
                static_url_path=cfg.FLASK.STATIC_URL_PATH,
                static_folder=cfg.FLASK.STATIC_FOLDER,
                template_folder=cfg.FLASK.TEMPLATE_FOLDER)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)

    return app
