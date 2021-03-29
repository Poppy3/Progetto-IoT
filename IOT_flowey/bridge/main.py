################################################################################
# Main script that spawns individual connection processes
#
################################################################################

# local
from gateway_connector import GatewayConnector
from server_connector import ServerConnector
from utils import compose_filename, purge_filename, debug, error, info, warning
import config as cfg

# standard libraries
from json import JSONDecodeError
from pathlib import Path
from serial import SerialException
from requests import ConnectionError
import datetime
import json
import multiprocessing as mp
import os
import signal
import time


def initializer():
    # Ignore CTRL+C in the worker process.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def run_unsent_data_worker(port):
    debug(f'run_unsent_data_worker() pid = {os.getpid()}')
    buffer_dir_path = Path(__file__).with_name('_' + purge_filename(port))
    srv_cnx = ServerConnector(suffix=port)

    while True:
        if buffer_dir_path.is_dir():
            for buffer_path in sorted(buffer_dir_path.glob(compose_filename(cfg.UNSENT_DATA_BUFFER_FILENAME, suffix='*'))):
                # read data and try to send it, keep unsent data
                with buffer_path.open('r+', buffering=1) as f:
                    delete_file = False
                    try:
                        data = json.load(f)
                    except JSONDecodeError:
                        error(f'Error while decoding {buffer_path.absolute()}. It will be deleted.')
                        delete_file = True
                    else:
                        tries = data.get('tries', 0)
                        try:
                            response = srv_cnx.send_plant_data(data)
                            if response is not None and response.status_code == 201:  # 201 - created
                                delete_file = True
                            else:
                                tries += 1
                        except ConnectionError:
                            tries += 1

                        if tries > cfg.UNSENT_DATA_MAX_TRIES:
                            warning(f'Exceeded max tries ({cfg.UNSENT_DATA_MAX_TRIES}) for {buffer_path.absolute()}. '
                                    f'It will be deleted.')
                            delete_file = True

                    if delete_file:
                        debug(f'Removing {buffer_path.absolute()}')
                        f.close()
                        buffer_path.unlink()  # delete file
                    else:
                        # keep file, but increment 'tries' value and save it
                        data['tries'] = tries
                        debug(f'run_unsent_data_worker - Writing {data} into buffer file')
                        f.seek(0)
                        json.dump(data, f, sort_keys=True)
                        f.truncate()
            # end for
        time.sleep(cfg.UNSENT_DATA_BUFFER_INTERVAL_TIME)


def run_bridge_worker(connection):
    debug(f'run_bridge_worker() pid = {os.getpid()}')
    port = connection["p"]
    baudrate = connection["b"]
    uuid = connection["id"]
    plant_type_name = connection["t"]
    debug(f'run_bridge_worker - Running run_gateway_connector with parameters: {connection}')

    try:
        gtw_cnx = GatewayConnector(port, baudrate)
        srv_cnx = ServerConnector(suffix=port)
        buffer_dir_path = Path(__file__).with_name('_' + purge_filename(port))
        buffer_dir_path.mkdir(parents=True, exist_ok=True)
        index = 0

        while True:
            debug('run_bridge_worker - Reading line from gateway connector...', 2)
            data = gtw_cnx.readline()
            debug(f'run_bridge_worker - Serial data received: {data}', 2)
            if data is None:
                warning('Serial data received was None. Reopening serial connection.')
                gtw_cnx.reopen()
                continue

            creation_date = datetime.datetime.now()

            data['plant_id'] = uuid
            data['plant_type_name'] = plant_type_name
            data['creation_date'] = creation_date.isoformat()
            data['bridge_id'] = cfg.BRIDGE_ID
            data['_index'] = index
            index += 1

            save_unsent_data = False
            try:
                debug(f'run_bridge_worker - Sending data = {data}')
                response = srv_cnx.send_plant_data(data)
                if response is not None:
                    debug(f'run_bridge_worker - Received response = ({response.status_code}) {response.content}', 2)
                    if response.status_code != 201:  # 201 - created
                        save_unsent_data = True
            except ConnectionError:
                save_unsent_data = True

            if save_unsent_data:
                buffer_path = buffer_dir_path / compose_filename(cfg.UNSENT_DATA_BUFFER_FILENAME,
                                                                 suffix=creation_date.strftime("%Y%m%d_%H%M%S"))
                try:
                    with buffer_path.open('w', buffering=1) as f:
                        debug(f'run_bridge_worker - Writing data to unsent_data buffer file {buffer_path.absolute()}')
                        json.dump(data, f, sort_keys=True)
                except FileNotFoundError:
                    error(f'FileNotFoundError for {buffer_path.absolute()}')
    except SerialException:
        error(f'Could not open serial connection to port={port}')
        raise


def main():
    debug(f'Running script with debug level = {cfg.DEBUG_LEVEL}')
    debug(f'main() pid = {os.getpid()}')
    p = Path(__file__).with_name(cfg.CONNECTIONS_STORAGE_FILENAME)
    debug(f'main - Opening connections storage file {p.absolute()}')
    try:
        with p.open('r') as f:
            try:
                connections = json.load(f)
                if type(connections) is not list:
                    error(f'Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}')
                    exit(-1)
                n = len(connections)
                if n == 0:
                    error(f'No connections registered in {p.absolute()}\n'
                          f'Try running "setup.py -h" script first')
                    exit(-1)
                info(f'Initializing {n} workers')
                bridge_pool = mp.Pool(processes=n, initializer=initializer)
                unsent_pool = mp.Pool(processes=n, initializer=initializer)
                try:
                    bridge_pool.map_async(run_bridge_worker, connections)
                    unsent_pool.map_async(run_unsent_data_worker, [connection["p"] for connection in connections])
                    while True:
                        # running forever. waiting for interrupt command.
                        time.sleep(999_999)
                except KeyboardInterrupt:
                    debug('main - Received KeyboardInterrupt')
                    info('Terminating spawned "run_bridge_worker()" and "run_unsent_data_worker()" workers')
                    bridge_pool.terminate()
                    bridge_pool.close()
                    unsent_pool.terminate()
                    unsent_pool.close()
                    exit(0)
                error('Reached unexpected code. Terminating pooled processes.')
                bridge_pool.terminate()
                bridge_pool.close()
                unsent_pool.terminate()
                unsent_pool.close()
                exit(-1)
            except ValueError:
                error(f'No connections registered in {p.absolute()}\n'
                      f'Try running "setup.py -h" first')
                exit(-1)
    except FileNotFoundError:
        error(f'File not found {p.absolute()}\n'
              f'Try running "setup.py -h" first')
        exit(-1)


if __name__ == '__main__':
    main()
