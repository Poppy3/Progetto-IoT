################################################################################
# Contiene il codice per gestire l'installazione di un nuovo
# gateway connector (=arduino) al bridge (=raspberry)
################################################################################

# local
from utils import debug, error
import config as cfg

# standard libraries
from json import JSONDecodeError
from pathlib import Path
from requests import ConnectionError
import argparse
import json
import requests
import uuid


parser = argparse.ArgumentParser(description='Register a new gateway connection or remove an existing one')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-l', '--list', help='List existing gateway connections', action='store_true')
group.add_argument('-a', '--add', help='Add a new gateway connection', action='store_true')
group.add_argument('-d', '--delete', help='Delete an existing gateway connection', action='store_true')
group.add_argument('-D', '--delete-all', help='Delete ALL existing gateway connection', action='store_true')
group.add_argument('-T', '--type-list', help='List all registered Plant Types', action='store_true')
parser.add_argument('-p', '--serial-port', type=str, help='Serial Port')
parser.add_argument('-b', '--serial-baudrate', type=int, help='Serial Baudrate')
parser.add_argument('-t', '--type', type=str, help='Plant Type')

args = parser.parse_args()

if args.add and (args.serial_baudrate is None or args.serial_port is None or args.type is None):
    parser.error("--add requires --serial-port and --serial-baudrate and --type")
if args.delete and (args.serial_baudrate is None or args.serial_port is None or args.type is None):
    parser.error("--delete requires --serial-port and --serial-baudrate and --type")

p = Path(__file__).with_name(cfg.CONNECTIONS_STORAGE_FILENAME)


def check_already_present(serial_port, serial_baudrate, conn_list):
    for elem in conn_list:
        if elem["p"] == serial_port and elem["b"] == serial_baudrate:
            return True
    return False


def generate_uuid():
    return uuid.uuid4().hex


def list_case():
    try:
        with p.open('r') as f:
            try:
                connections = json.load(f)
                if not isinstance(connections, list):
                    error(f'Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}')
                    exit(-1)
                print('Listing existing connections:')
                if len(connections) == 0:
                    print('-- EMPTY --')
                else:
                    for idx, connection in enumerate(connections, start=1):
                        print(f'{idx} - Serial Port: {connection["p"]}'
                              f' - Serial Baudrate: {connection["b"]}'
                              f' - Type: {connection["t"]}'
                              f' - UUID: {connection["id"]}')
                exit(0)
            except ValueError:
                print('Listing existing connections:\n'
                      '-- EMPTY --')
                exit(0)
    except FileNotFoundError:
        print('Listing existing connections:\n'
              '-- EMPTY --')
        with p.open('w') as f:
            json.dump([], f)
        exit(0)


def add_case():
    new_connection = {"p": args.serial_port, "b": args.serial_baudrate, "t": args.type, "id": generate_uuid()}
    try:
        with p.open('r+') as f:
            try:
                connections = json.load(f)
                if not isinstance(connections, list):
                    error(f'Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}')
                    exit(-1)
                if check_already_present(new_connection["p"], new_connection["b"], connections):
                    error(f'It already exists a connection with '
                          f'serial-port={new_connection["p"]} and '
                          f'serial-baudrate={new_connection["b"]}')
                    exit(-1)
                connections.append(new_connection)
                f.seek(0)
                f.truncate(0)
                json.dump(connections, f)
                print(f'Added connection with:\n'
                      f' serial-port={new_connection["p"]}\n'
                      f' serial-baudrate={new_connection["b"]}\n'
                      f' type={new_connection["t"]}\n'
                      f' uuid={new_connection["id"]}')
                exit(0)
            except ValueError as e:
                f.seek(0)
                f.truncate(0)
                json.dump([new_connection], f)
                print(f'Added connection with:\n'
                      f' serial-port={new_connection["p"]}\n'
                      f' serial-baudrate={new_connection["b"]}\n'
                      f' type={new_connection["t"]}\n'
                      f' uuid={new_connection["id"]}')
                exit(0)
    except FileNotFoundError as e:
        with p.open('w') as f:
            f.seek(0)
            f.truncate(0)
            json.dump([new_connection], f)
            print(f'Added connection with:\n'
                  f' serial-port={new_connection["p"]}\n'
                  f' serial-baudrate={new_connection["b"]}\n'
                  f' type={new_connection["t"]}\n'
                  f' uuid={new_connection["id"]}')
            exit(0)


def delete_case():
    to_be_deleted = {"p": args.serial_port, "b": args.serial_baudrate}
    try:
        with p.open('r+') as f:
            try:
                connections = json.load(f)
                if not isinstance(connections, list):
                    error(f'Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}.')
                    exit(-1)
                if not check_already_present(to_be_deleted["p"], to_be_deleted["b"], connections):
                    error(f'It does not already exists a connection with '
                          f'serial-port={to_be_deleted["p"]} and '
                          f'serial-baudrate={to_be_deleted["b"]}')
                    exit(-1)
                connections.remove(to_be_deleted)
                f.seek(0)
                f.truncate(0)
                json.dump(connections, f)
                print(f'Deleted connection with:\n'
                      f' serial-port={to_be_deleted["p"]}\n'
                      f' serial-baudrate={to_be_deleted["b"]}\n'
                      f' type={to_be_deleted["t"]}\n'
                      f' uuid={to_be_deleted["id"]}')
                exit(0)
            except ValueError:
                error(f'It does not already exists a connection with '
                      f'serial-port={to_be_deleted["p"]} and '
                      f'serial-baudrate={to_be_deleted["b"]}')
                exit(-1)
    except FileNotFoundError as e:
        error(f'It does not already exists a connection with '
              f'serial-port={to_be_deleted["p"]} and '
              f'serial-baudrate={to_be_deleted["b"]}')
        with p.open('w') as f:
            json.dump([], f)
        exit(-1)


def delete_all_case():
    with p.open('w') as f:
        f.seek(0)
        f.truncate(0)
        json.dump([], f)
        print(f'Deleted all registered connections')
        exit(0)


def type_list_case():
    url = cfg.SERVER_CONNECTOR.PROTOCOL + cfg.SERVER_CONNECTOR.HOST
    url += f':{cfg.SERVER_CONNECTOR.PORT}' if cfg.SERVER_CONNECTOR.PORT is not None else ''
    url += cfg.SERVER_CONNECTOR.ENDPOINTS.PLANT_TYPE
    debug(f'Trying to retrieve plant_types from {url}')
    try:
        response = requests.get(url)
        parsed = response.json()
        print('Listing all registered Plant Types:')
        for idx, plant_type in enumerate(parsed, start=1):
            print(f'{idx} - {plant_type["name"]}')
        exit(0)
    except ConnectionError as e:
        debug(f'Encountered ConnectionError {e}')
    except KeyError as e:
        debug(f'Encountered KeyError {e}')
    except JSONDecodeError as e:
        debug(f'Encountered JSONDecodeError {e}')
    except Exception as e:
        debug(f'Caught unexpected exception - {type(e)}\n{e}')
    error(f'Could not retrieve plant_types from {url}')
    exit(-1)


if args.list:
    list_case()
elif args.add:
    add_case()
elif args.delete:
    delete_case()
elif args.delete_all:
    delete_all_case()
elif args.type_list:
    type_list_case()
