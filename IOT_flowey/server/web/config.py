import os

# flask configuration file
BUNDLE_ERRORS = True
DEBUG = True
SECRET_KEY = 'This1Is2A3Secret4Key5'
TEMPLATES_AUTO_RELOAD = True

# Database hostato da pythonanywhere
# SQLALCHEMY_DATABASE_URI = 'mysql://iotproject:XccVBVp4kkUwFdB@iotproject.mysql.eu.pythonanywhere-services.com/iotproject$default'
# Database hostato da freemysqlhosting
# SQLALCHEMY_DATABASE_URI = 'mysql://sql11398075:X3LHKv2R4k@sql11.freemysqlhosting.net/sql11398075'
# Database locale
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dev.sqlite3')
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 250,
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

RESTFUL_PREFIX = '/api/v1'

# TELEFLASK_API_KEY = '1744886816:AAF4Xz6dNJmfgooDUK0c_7E9zLo4pES-I1A'
# TELEFLASK_HOSTNAME = 'localhost'
