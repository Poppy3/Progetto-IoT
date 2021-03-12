import os

# flask configuration file
DEBUG = True
TEMPLATES_AUTO_RELOAD = True

#SQLALCHEMY_DATABASE_URI = 'mysql://sql11398075:X3LHKv2R4k@sql11.freemysqlhosting.net/sql11398075'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dev.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False

RESTFUL_PREFIX = '/api/v1'