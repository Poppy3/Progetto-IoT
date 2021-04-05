################################################################################
# Controllore della comunicazione col server (=pc/datacenter)
# Mette a disposizione delle funzioni per leggere/scrivere da/verso il server
################################################################################

# local
from utils import compose_filename, error
import config as cfg

# standard libraries
from pathlib import Path
import json
import requests


class ServerConnector:
    def __init__(self, protocol=cfg.SERVER_CONNECTOR.PROTOCOL,
                 host=cfg.SERVER_CONNECTOR.HOST,
                 port=cfg.SERVER_CONNECTOR.PORT,
                 local_mode=cfg.SERVER_CONNECTOR.LOCAL_MODE,
                 suffix=None,
                 log_path=None):
        self._protocol = protocol
        self._host = host
        self._port = port
        self._local_mode = local_mode
        self._suffix = suffix
        self._log_path = log_path

    def set_host(self, host):
        self._host = host

    def set_port(self, port):
        self._port = port

    def send_plant_data(self, data):
        if self._local_mode:
            return self._save_data_to_local_file(data)
        else:
            url = self._get_url(endpoint=cfg.SERVER_CONNECTOR.ENDPOINTS.PLANT_DATA)
            return self._call_api(url=url, data=data, method='POST')

    def _get_url(self, endpoint=None):
        url = self._protocol + self._host
        if self._port is not None:
            url = url + f':{self._port}'
        if endpoint is not None:
            url = url + endpoint
        return url

    @staticmethod
    def _call_api(url, data, method='GET'):
        assert method is not None and isinstance(method, str), \
            "method must be provided with a value from ['GET', 'POST', 'PUT', 'DELETE']"
        method = method.upper()
        assert method in ['GET', 'POST', 'PUT', 'DELETE'], \
            "method must be provided with a value from ['GET', 'POST', 'PUT', 'DELETE']"

        if method == 'GET':
            return requests.get(url=url, params=data)
        if method == 'POST':
            return requests.post(url=url, json=data)
        if method == 'PUT':
            return requests.put(url=url, json=data)
        if method == 'DELETE':
            return requests.delete(url=url)

    def _save_data_to_local_file(self, data):
        filename = compose_filename(cfg.SERVER_CONNECTOR.LOCAL_FILENAME, self._suffix)
        p = Path(__file__).with_name(filename)
        try:
            with p.open('a') as f:
                json.dump(data, f)
                f.write('\n')
        except FileNotFoundError:
            error(f'ServerConnector._save_data_to_local_file() - FileNotFoundError for {p.absolute()}',
                  path=self._log_path)
