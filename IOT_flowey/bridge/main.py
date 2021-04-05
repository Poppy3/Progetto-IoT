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
    log_path = Path(__file__).with_name(compose_filename(cfg.LOGGING.UNSENT_DATA_WORKER_FILENAME,
                                                         suffix=purge_filename(port)))
    info('- - - - - - - - - - - - - - - - - - - -', path=log_path)
    info(f'run_unsent_data_worker() - pid = {os.getpid()}', path=log_path)
    buffer_dir_path = Path(__file__).with_name('_' + purge_filename(port))
    srv_cnx = ServerConnector(suffix=port, log_path=log_path)

    while True:
        if buffer_dir_path.is_dir():
            for buffer_path in sorted(buffer_dir_path.glob(compose_filename(cfg.UNSENT_DATA_BUFFER_FILENAME,
                                                                            suffix='*'))):
                # read data and try to send it, keep unsent data
                with buffer_path.open('r+', buffering=1) as f:
                    delete_file = False
                    try:
                        data = json.load(f)
                    except JSONDecodeError:
                        error(f'run_unsent_data_worker() - Error while decoding {buffer_path.absolute()}. '
                              f'It will be deleted.', path=log_path)
                        delete_file = True
                    else:
                        tries = data.get('tries', 0)
                        try:
                            response = srv_cnx.send_plant_data(data)
                            if response is not None and response.status_code == 201:  # 201 - created
                                info(f'run_unsent_data_worker() - Managed to send plant_data from '
                                     f'{buffer_path.absolute()}. The file is not needed anymore and will be deleted.',
                                     path=log_path)
                                delete_file = True
                        except ConnectionError as e:
                            warning(f'run_unsent_data_worker() - ConnectionError {e} '
                                    f'raised for {buffer_path.absolute()}', path=log_path)

                        if tries >= cfg.UNSENT_DATA_MAX_TRIES:
                            warning(f'run_unsent_data_worker() - Exceeded max tries ({cfg.UNSENT_DATA_MAX_TRIES}) for '
                                    f'{buffer_path.absolute()}. It will be deleted.', path=log_path)
                            delete_file = True

                    if delete_file:
                        debug(f'run_unsent_data_worker() - Removing {buffer_path.absolute()}', path=log_path)
                        f.close()
                        buffer_path.unlink()  # delete file
                    else:
                        # keep file, but increment 'tries' value and save it
                        data['tries'] = tries + 1
                        debug(f'run_unsent_data_worker() - Writing {data} into buffer file', path=log_path)
                        f.seek(0)
                        json.dump(data, f, sort_keys=True)
                        f.truncate()
            # end for
        time.sleep(cfg.UNSENT_DATA_BUFFER_INTERVAL_TIME)


def run_bridge_worker(connection):
    port = connection["p"]
    baudrate = connection["b"]
    uuid = connection["id"]
    plant_type_name = connection["t"]
    log_path = Path(__file__).with_name(compose_filename(cfg.LOGGING.BRIDGE_WORKER_FILENAME,
                                                         suffix=purge_filename(port)))
    info('- - - - - - - - - - - - - - - - - - - -', path=log_path)
    info(f'run_bridge_worker() - pid = {os.getpid()}', path=log_path)
    debug(f'run_bridge_worker() - Running run_gateway_connector with parameters: {connection}', path=log_path)

    try:
        gtw_cnx = GatewayConnector(port, baudrate, log_path=log_path)
        srv_cnx = ServerConnector(suffix=port, log_path=log_path)
        buffer_dir_path = Path(__file__).with_name('_' + purge_filename(port))
        buffer_dir_path.mkdir(parents=True, exist_ok=True)
        index = 0

        while True:
            debug('run_bridge_worker() - Reading line from gateway connector...', 2, path=log_path)
            data = gtw_cnx.readline()
            debug(f'run_bridge_worker() - Serial data received: {data}', 2, path=log_path)
            if data is None:
                warning('run_bridge_worker() - Serial data received was None. Consider restarting serial connection.',
                        path=log_path)
                # gtw_cnx.reopen()
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
                debug(f'run_bridge_worker() - Sending data = {data}', path=log_path)
                response = srv_cnx.send_plant_data(data)
                if response is not None:
                    debug(f'run_bridge_worker() - Received response = ({response.status_code}) {response.content}', 2,
                          path=log_path)
                    if response.status_code != 201:  # 201 - created
                        save_unsent_data = True
            except ConnectionError:
                save_unsent_data = True

            if save_unsent_data:
                buffer_path = buffer_dir_path / compose_filename(cfg.UNSENT_DATA_BUFFER_FILENAME,
                                                                 suffix=creation_date.strftime("%Y%m%d_%H%M%S"))
                try:
                    with buffer_path.open('w', buffering=1) as f:
                        debug(f'run_bridge_worker() - Writing data to unsent_data buffer file {buffer_path.absolute()}',
                              path=log_path)
                        json.dump(data, f, sort_keys=True)
                except FileNotFoundError:
                    error(f'run_bridge_worker() - FileNotFoundError for {buffer_path.absolute()}', path=log_path)
    except SerialException:
        error(f'run_bridge_worker() - Could not open serial connection to port={port}', path=log_path)
        raise


def main():
    log_path = Path(__file__).with_name(cfg.LOGGING.MAIN_FILENAME)
    info('- - - - - - - - - - - - - - - - - - - -', path=log_path)
    info(f'main() - Running script with debug level = {cfg.LOGGING.DEBUG_LEVEL}', path=log_path)
    info(f'main() - pid = {os.getpid()}', path=log_path)
    conn_path = Path(__file__).with_name(cfg.CONNECTIONS_STORAGE_FILENAME)
    info(f'main() - Opening connections storage file {conn_path.absolute()}', path=log_path)
    try:
        with conn_path.open('r') as f:
            try:
                connections = json.load(f)
                if type(connections) is not list:
                    error(f'main() - Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}', path=log_path)
                    exit(-1)
                n = len(connections)
                if n == 0:
                    error(f'main() - No connections registered in {conn_path.absolute()}\n'
                          f'Try running "setup.py -h" script first', path=log_path)
                    exit(-1)
                info(f'main() - Initializing {n} workers', path=log_path)
                bridge_pool = mp.Pool(processes=n, initializer=initializer)
                unsent_pool = mp.Pool(processes=n, initializer=initializer)
                try:
                    bridge_pool.map_async(run_bridge_worker, connections)
                    unsent_pool.map_async(run_unsent_data_worker, [connection["p"] for connection in connections])
                    while True:
                        # running forever. waiting for interrupt command.
                        time.sleep(999_999)
                except KeyboardInterrupt:
                    debug('main() - Received KeyboardInterrupt', path=log_path)
                    info('main() - Terminating spawned "run_bridge_worker()" and "run_unsent_data_worker()" workers',
                         path=log_path)
                    bridge_pool.terminate()
                    bridge_pool.close()
                    unsent_pool.terminate()
                    unsent_pool.close()
                    exit(0)
                error('main() - Reached unexpected code. Terminating pooled processes.', path=log_path)
                bridge_pool.terminate()
                bridge_pool.close()
                unsent_pool.terminate()
                unsent_pool.close()
                exit(-1)
            except ValueError:
                error(f'main() - No connections registered in {conn_path.absolute()}\n'
                      f'Try running "setup.py -h" first', path=log_path)
                exit(-1)
    except FileNotFoundError:
        error(f'main() - File not found {conn_path.absolute()}\n'
              f'Try running "setup.py -h" first', path=log_path)
        exit(-1)


if __name__ == '__main__':
    main()
