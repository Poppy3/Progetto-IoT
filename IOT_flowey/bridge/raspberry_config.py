################################################################################
# File che contiene i valori di configurazione usati dai vari moduli di 'bridge'
# è il file coi valori utilizzati concretamente dal raspberry pi di damiano
################################################################################

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
    LOCAL_FILENAME = 'local_plant_data.csv'
    class ENDPOINTS:
        PLANT_DATA = '/api/v1/plant_data'
        PLANT_TYPE = '/api/v1/plant_type'


BRIDGE_ID = 'RASPBERRY001'
CONNECTIONS_STORAGE_FILENAME = 'connections_storage.json'
LOCK_TIMEOUT = 1
UNSENT_DATA_BUFFER_INTERVAL_TIME = 3600  # 1h worth of seconds (60m * 60s)
UNSENT_DATA_BUFFER_FILENAME = 'unsent_data.json'
UNSENT_DATA_MAX_TRIES = 50
DEBUG_LEVEL = 0  # 0: no debug, 1: base debug, 2: verbose debug