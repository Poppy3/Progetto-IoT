################################################################################
# File che contiene i valori di configurazione usati dai vari moduli di 'bridge'
# è il file coi valori utilizzati concretamente dal raspberry pi di damiano
################################################################################

class LOGGING:
    DEBUG_LEVEL = 0  # 0: no debug, 1: base debug, 2: verbose debug
    MAIN_FILENAME = 'main.log'
    BRIDGE_WORKER_FILENAME = 'bridge_worker.log'
    UNSENT_DATA_WORKER_FILENAME = 'unsent_data_worker.log'


class GATEWAY_CONNECTOR:
    LOCAL_MODE = False
    READ_MAX_TRIES = 10
    READ_INTERVAL_TIME = 5.0  # seconds
    TIMEOUT = None  # seconds


class SERVER_CONNECTOR:
    PROTOCOL = 'https://'
    HOST = 'iotproject.eu.pythonanywhere.com'
    PORT = None
    LOCAL_MODE = False
    LOCAL_FILENAME = 'local_plant_data.txt'

    class ENDPOINTS:
        PLANT_DATA = '/api/v1/plant_data'
        PLANT_TYPE = '/api/v1/plant_type'


class TELEGRAM_BOT:
    ADMIN_CHAT_ID = '353051365'
    API_KEY = '1744886816:AAF4Xz6dNJmfgooDUK0c_7E9zLo4pES-I1A'


class UNSENT_DATA:
    ALERT_THRESHOLD = 42  # number of tries after which an alert message will be sent
    BUFFER_FILENAME = 'unsent_data.json'
    INTERVAL_TIME = 3600  # 1h worth of seconds (60m * 60s)
    MAX_TRIES = 50


BRIDGE_ID = 'RASPBERRY001'
CONNECTIONS_STORAGE_FILENAME = 'connections_storage.json'
PID_FILENAME = 'bridge.pid'
