################################################################################
# Main script that spawns individual connection processes
#
################################################################################

# local
from gateway_connector import GatewayConnector
from server_connector import ServerConnector
from utils import debug
import config as cfg

# standard libraries
from pathlib import Path
from serial import SerialException
from requests import Response
import datetime
import json
import multiprocessing as mp
import signal
import time


def initializer():
    # Ignore CTRL+C in the worker process.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def run_gateway_connector(connection):
    serial_port = connection["p"]
    serial_number = connection["n"]
    uuid = connection["id"]
    plant_type_name = connection["t"]
    debug(f'Running run_gateway_connector with parameters: {connection}')

    try:
        gtw_cnx = GatewayConnector(serial_port, serial_number)

        # TODO quando si usa ngrok si può rimuovere il parametro local_mode_suffix da qui sotto
        srv_cnx = ServerConnector(local_mode_suffix=f'{serial_port}-{serial_number}')

        while True:
            try:
                debug('Reading line from gateway connector...', 2)
                data = gtw_cnx.readline()
                debug(f'Serial data received: {data}', 2)
                if data is not None:
                    data['plant_id'] = uuid
                    data['plant_type_name'] = plant_type_name
                    data['creation_date'] = datetime.datetime.now().isoformat()
                    data['bridge_id'] = cfg.BRIDGE_ID

                    debug(f'Sending data = {data}')
                    response = srv_cnx.send_plant_data(data)
                    if isinstance(response, Response):
                        debug(f'Received response = [{response.status_code}] {response.content}')

            except Exception as e:
                print(f'ERROR - Raised exception {e}\n{e.args}')
                raise e
    except SerialException as e:
        print(f'ERROR - could not open connection to serial-port={serial_port} and serial-number={serial_number}')


if __name__ == '__main__':
    debug(f'Running script with debug level = {cfg.DEBUG}')
    p = Path(__file__).with_name(cfg.CONNECTIONS_STORAGE_FILENAME)
    debug(f'Opening connections storage file {p.absolute()}')
    try:
        with p.open('r') as f:
            try:
                connections = json.load(f)
                if type(connections) is not list:
                    print(f'ERROR - Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}')
                    exit(-1)
                if len(connections) == 0:
                    print(f'ERROR - no connections registered in {p.absolute()}\n'
                          f'Try running "setup.py -h" first')
                    exit(-1)
                print(f'INFO - Initializing {len(connections)} workers')
                pool = mp.Pool(processes=len(connections), initializer=initializer)
                try:
                    pool.map_async(run_gateway_connector, connections)
                    while True:
                        # running forever. waiting for interrupt command.
                        pass
                except KeyboardInterrupt:
                    debug('Received KeyboardInterrupt')
                    print('INFO - Terminating spawned "run_gateway_connector" workers')
                    pool.terminate()
                    pool.close()
                    exit(0)
                print('ERROR - Reached unexpected code. Terminating pooled processes.')
                pool.terminate()
                pool.close()
                exit(-1)
            except ValueError:
                print(f'ERROR - no connections registered in {p.absolute()}\n'
                      f'Try running "setup.py -h" first')
                exit(-1)
    except FileNotFoundError:
        print(f'ERROR - not found file {p.absolute()}\n'
              f'Try running "setup.py -h" first')
        exit(-1)
