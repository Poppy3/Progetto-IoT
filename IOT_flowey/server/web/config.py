import os

###############################################################################
# Flask configuration
###############################################################################
BUNDLE_ERRORS = True
DEBUG = True
SECRET_KEY = 'This1Is2A3Secret4Key5'
TEMPLATES_AUTO_RELOAD = True


###############################################################################
# Extension: SQLAlchemy configuration
###############################################################################
# Database local machine
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dev.sqlite3')
# Database hosted by freemysqlhosting
#SQLALCHEMY_DATABASE_URI = 'mysql://sql11398075:X3LHKv2R4k@sql11.freemysqlhosting.net/sql11398075'
# Database hosted by pythonanywhere
#SQLALCHEMY_DATABASE_URI = 'mysql://iotproject:XccVBVp4kkUwFdB@iotproject.mysql.eu.pythonanywhere-services.com/iotproject$default'
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 250,
}
SQLALCHEMY_TRACK_MODIFICATIONS = False


###############################################################################
# Extension: sqlalchemy configuration
###############################################################################
RESTFUL_PREFIX = '/api/v1'


###############################################################################
# Extension: telegram_bot configuration
###############################################################################
TELEGRAM_API_KEY = '1744886816:AAF4Xz6dNJmfgooDUK0c_7E9zLo4pES-I1A'
#TELEGRAM_APP_PUBLIC_HOSTNAME = 'http://localhost:8080'  # local hostname
#TELEGRAM_APP_PUBLIC_HOSTNAME = 'https://iotproject.eu.pythonanywhere.com'  # hostname provided by hosting service
#TELEGRAM_APP_PATH_PREFIX = '/telegram_bot'
TELEGRAM_BASE_URL = 'http://localhost:8081/bot'  # put None to use telegram real api and not the local one
#TELEGRAM_BASE_URL = None  # Use in hosted app
