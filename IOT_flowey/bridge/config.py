################################################################################
# File che contiene i valori di configurazione usati dai vari moduli di 'bridge'
################################################################################

class GATEWAY_CONNECTOR:
    LOCAL_MODE = True  # TODO - impostare a False per la comunicazione con arduino
    READ_MAX_TRIES = 10
    READ_INTERVAL_TIME = 2.0
    READ_TOLERANCE_TIME = 0.33


class SERVER_CONNECTOR:
    PROTOCOL = 'http://'  # TODO - da impostare con quello dato da ngrok
    HOST = '127.0.0.1'  # TODO - da impostare con quello dato da ngrok
    PORT = '8080'  # TODO - da impostare con quello dato da ngrok
    LOCAL_MODE = False  # TODO - impostare a False per la comunicazione con ngrok
    LOCAL_FILENAME = 'local_plant_data.csv'
    class ENDPOINTS:
        PLANT_DATA = '/api/v1/plant_data'


BRIDGE_ID = 'RASPBERRY001'
CONNECTIONS_STORAGE_FILENAME = 'connections_storage.json'
DEBUG = True
