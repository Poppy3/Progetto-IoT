################################################################################
# File che contiene i valori di configurazione usati dai vari moduli di 'bridge'
################################################################################

class GATEWAY_CONNECTOR:
    LOCAL_MODE = True  # TODO - impostare a False per la comunicazione con arduino
    READ_MAX_TRIES = 10
    READ_INTERVAL_TIME = 2.0  # seconds
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


BRIDGE_ID = 'RASPBERRY001'
CONNECTIONS_STORAGE_FILENAME = 'connections_storage.json'
LOCK_TIMEOUT = 10
UNSENT_DATA_BUFFER_INTERVAL_TIME = 5  # 1h worth of seconds (60m * 60s)
UNSENT_DATA_BUFFER_DIM = 1440  # 10 days worth of data lines (1440 = 10d * 24h * 60m / 10m)
UNSENT_DATA_BUFFER_FILENAME = 'unsent_data.txt'
DEBUG_LEVEL = 1  # 0: no debug, 1: base debug, 2: verbose debug
