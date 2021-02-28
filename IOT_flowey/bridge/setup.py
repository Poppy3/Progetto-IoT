################################################################################
# Contiene il codice per gestire l'installazione di un nuovo
# gateway connector (=arduino) al bridge (=raspberry)
################################################################################

# local
import config as cfg

# standard libraries
import argparse
import json
import uuid
from pathlib import Path


parser = argparse.ArgumentParser(description='Register a new gateway connection or remove an existing one')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-l', '--list', help='List existing gateway connections', action='store_true')
group.add_argument('-a', '--add', help='Add a new gateway connection', action='store_true')
group.add_argument('-d', '--delete', help='Delete an existing gateway connection', action='store_true')
group.add_argument('-D', '--delete-all', help='Delete ALL existing gateway connection', action='store_true')
parser.add_argument('-p', '--serial-port', type=str, help='Serial Port number')
parser.add_argument('-n', '--serial-number', type=int, help='Serial Number')
parser.add_argument('-t', '--type', type=str, help='Plant Type')

args = parser.parse_args()

if args.add and (args.serial_number is None or args.serial_port is None or args.type is None):
    parser.error("--add requires --serial-port and --serial-number and --type")
if args.delete and (args.serial_number is None or args.serial_port is None or args.type is None):
    parser.error("--delete requires --serial-port and --serial-number and --type")

p = Path(__file__).with_name(cfg.CONNECTIONS_STORAGE_FILENAME)


def check_already_present(serial_port, serial_number, connections):
    for elem in connections:
        if elem["p"] == serial_port and elem["n"] == serial_number:
            return True
    return False


def generate_uuid():
    return uuid.uuid4().hex


if args.list:
    try:
        with p.open('r') as f:
            try:
                connections = json.load(f)
                if type(connections) is not list:
                    print(f'ERROR - Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}')
                    exit(-1)
                print('Listing existing connections:')
                if len(connections) == 0:
                    print('-- EMPTY --')
                else:
                    for idx, connection in enumerate(connections, start=1):
                        print(f'{idx} - Serial Port: {connection["p"]}'
                              f' - Serial Number: {connection["n"]}'
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

elif args.add:
    try:
        new_connection = {"p": args.serial_port, "n": args.serial_number, "t": args.type.lower(), "id": generate_uuid()}
        with p.open('r+') as f:
            try:
                connections = json.load(f)
                if type(connections) is not list:
                    print(f'ERROR - Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n' 
                          f'Was expecting list type, but found {type(connections)}')
                    exit(-1)
                if check_already_present(new_connection["p"], new_connection["n"], connections):
                    print(f'ERROR - It already exists a connection with '
                          f'serial-port={new_connection["p"]} and '
                          f'serial-number={new_connection["n"]}')
                    exit(-1)
                connections.append(new_connection)
                f.seek(0)
                f.truncate(0)
                json.dump(connections, f)
                print(f'Added connection with:\n'
                      f' serial-port={new_connection["p"]}\n'
                      f' serial-number={new_connection["n"]}\n'
                      f' type={new_connection["t"]}\n'
                      f' uuid={new_connection["id"]}')
                exit(0)
            except ValueError as e:
                f.seek(0)
                f.truncate(0)
                json.dump([new_connection], f)
                print(f'Added connection with:\n'
                      f' serial-port={new_connection["p"]}\n'
                      f' serial-number={new_connection["n"]}\n'
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
                  f' serial-number={new_connection["n"]}\n'
                  f' type={new_connection["t"]}\n'
                  f' uuid={new_connection["id"]}')
            exit(0)

elif args.delete:
    try:
        to_be_deleted = {"p": args.serial_port, "n": args.serial_number}
        with p.open('r+') as f:
            try:
                connections = json.load(f)
                if type(connections) is not list:
                    print(f'ERROR - Error in contents of file {cfg.CONNECTIONS_STORAGE_FILENAME}.\n'
                          f'Was expecting list type, but found {type(connections)}.')
                    exit(-1)
                if not check_already_present(to_be_deleted["p"], to_be_deleted["n"], connections):
                    print(f'ERROR - It does not already exists a connection with '
                          f'serial-port={to_be_deleted["p"]} and '
                          f'serial-number={to_be_deleted["n"]}')
                    exit(-1)
                connections.remove(to_be_deleted)
                f.seek(0)
                f.truncate(0)
                json.dump(connections, f)
                print(f'Deleted connection with:\n'
                      f' serial-port={to_be_deleted["p"]}\n'
                      f' serial-number={to_be_deleted["n"]}\n'
                      f' type={to_be_deleted["t"]}\n'
                      f' uuid={to_be_deleted["id"]}')
                exit(0)
            except ValueError:
                print(f'ERROR - It does not already exists a connection with '
                      f'serial-port={to_be_deleted["p"]} and '
                      f'serial-number={to_be_deleted["n"]}')
                exit(-1)
    except FileNotFoundError as e:
        print(f'ERROR - It does not already exists a connection with '
              f'serial-port={to_be_deleted["p"]} and '
              f'serial-number={to_be_deleted["n"]}')
        with p.open('w') as f:
            json.dump([], f)
        exit(-1)

elif args.delete_all:
    with p.open('w') as f:
        f.seek(0)
        f.truncate(0)
        json.dump([], f)
        print(f'Deleted all registered connections')
        exit(0)
