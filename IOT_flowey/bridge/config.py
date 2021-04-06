################################################################################
# File che contiene i valori di configurazione usati dai vari moduli di 'bridge'
################################################################################

class LOGGING:
    DEBUG_LEVEL = 1  # 0: no debug, 1: base debug, 2: verbose debug
    MAIN_FILENAME = 'main.log'
    BRIDGE_WORKER_FILENAME = 'bridge_worker.log'
    UNSENT_DATA_WORKER_FILENAME = 'unsent_data_worker.log'


class GATEWAY_CONNECTOR:
    LOCAL_MODE = True  # TODO - impostare a False per la comunicazione con arduino
    READ_MAX_TRIES = 10
    READ_INTERVAL_TIME = 5.0  # seconds
    TIMEOUT = None  # seconds


class SERVER_CONNECTOR:
    PROTOCOL = 'http://'  # TODO - da impostare con quello dato da ngrok
    HOST = '127.0.0.1'  # TODO - da impostare con quello dato da ngrok
    PORT = '8080'  # TODO - da impostare con quello dato da ngrok
    LOCAL_MODE = False  # TODO - impostare a False per la comunicazione con ngrok
    LOCAL_FILENAME = 'local_plant_data.txt'
    class ENDPOINTS:
        PLANT_DATA = '/api/v1/plant_data'
        PLANT_TYPE = '/api/v1/plant_type'


class TELEGRAM_BOT:
    API_KEY ='1744886816:AAF4Xz6dNJmfgooDUK0c_7E9zLo4pES-I1A'


BRIDGE_ID = 'RASPBERRY001'
CONNECTIONS_STORAGE_FILENAME = 'connections_storage.json'
PID_FILENAME = 'bridge.pid'
UNSENT_DATA_BUFFER_INTERVAL_TIME = 3600  # 1h worth of seconds (60m * 60s)
UNSENT_DATA_BUFFER_FILENAME = 'unsent_data.json'
UNSENT_DATA_MAX_TRIES = 50
