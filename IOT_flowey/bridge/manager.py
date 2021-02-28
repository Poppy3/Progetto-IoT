################################################################################
# Main script that spawns individual connection processes
#
################################################################################

# local
import config as cfg
from gateway_connector import GatewayConnector
from utils import debug

# standard libraries
import json
import multiprocessing as mp
from pathlib import Path
from serial import SerialException


def run_gateway_connector(connection):
    serial_port = connection["p"]
    serial_number = connection["n"]
    debug(f'Running run_gateway_connector with serial-port={serial_port} and serial-number={serial_number}')
    try:
        connector = GatewayConnector(serial_port, serial_number)
        while True:
            try:
                data = connector.readline()
                debug(f'Serial data received: {data}')
                if data is not None:
                    # TODO
                    pass
            except Exception as e:
                print(f'ERROR - Raised exception {e}\n{e.args}')
                break
    except SerialException as e:
        print(f'ERROR - could not open connection to serial-port={serial_port} and serial-number={serial_number}')


if __name__ == '__main__':
    p = Path(__file__).with_name(cfg.CONNECTIONS_STORAGE_FILENAME)
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
                with mp.Pool(len(connections)) as pool:
                    pool.map(run_gateway_connector, connections)
                exit(0)
            except ValueError:
                print(f'ERROR - no connections registered in {p.absolute()}\n'
                      f'Try running "setup.py -h" first')
                exit(-1)
    except FileNotFoundError:
        print(f'ERROR - not found file {p.absolute()}\n'
              f'Try running "setup.py -h" first')
        exit(-1)
