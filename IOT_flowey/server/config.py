################################################################################
# File che contiene i valori di configurazione usati dai vari moduli di 'server'
################################################################################

class FLASK:
    HOST = '127.0.0.1'
    PORT = 8080
    DEBUG = True
    INSTANCE_RELATIVE_CONFIG = True
    STATIC_URL_PATH = ''
    STATIC_FOLDER = 'web/static'
    TEMPLATE_FOLDER = 'web/templates'
    TEMPLATES_AUTO_RELOAD = True


class MYSQL:
    HOST = "localhost"
    USER = "root"
    PASSWORD = "asiadamianomarco"
    DATABASE_NAME = "progetto_iot"


DEBUG = True
