################################################################################
# Controllore della comunicazione col server (=pc/datacenter)
# Mette a disposizione delle funzioni per leggere/scrivere da/verso il server
################################################################################

# local
import config as cfg

# standard libraries
from pathlib import Path
import requests


def _build_filename(filename, suffix):
    assert isinstance(filename, str), 'filename must be a string'
    assert isinstance(suffix, str) or suffix is None, 'suffix, when not None, must be a string'

    if suffix is not None:
        return '{0}_{2}.{1}'.format(*filename.rsplit('.', 1), suffix)
    return filename


class ServerConnector:
    def __init__(self, protocol=cfg.SERVER_CONNECTOR.PROTOCOL,
                 host=cfg.SERVER_CONNECTOR.HOST,
                 port=cfg.SERVER_CONNECTOR.PORT,
                 local_mode=cfg.SERVER_CONNECTOR.LOCAL_MODE,
                 local_mode_suffix=None):
        self._protocol = protocol
        self._host = host
        self._port = port
        self._local_mode = local_mode
        self._local_mode_suffix = local_mode_suffix

    def set_host(self, host):
        self._host = host

    def set_port(self, port):
        self._port = port

    def send_plant_data(self, data):
        if self._local_mode:
            return self._save_data_to_local_file(data)
        else:
            url = self._get_url(endpoint=cfg.SERVER_CONNECTOR.ENDPOINTS.PLANT_DATA)
            return self._call_api(url, data, method='POST')

    def _get_url(self, endpoint=None):
        url = self._protocol + self._host
        if self._port is not None:
            url = url + f':{self._port}'
        if endpoint is not None:
            url = url + endpoint
        return url

    def _call_api(self, url, data, method='GET'):
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
        filename = _build_filename(cfg.SERVER_CONNECTOR.LOCAL_FILENAME, self._local_mode_suffix)
        p = Path(__file__).with_name(filename)
        write_header = not p.exists()
        try:
            with p.open('a') as f:
                if write_header:
                    f.write('"plant_id","plant_type_name","creation_date","bridge_id"'
                            '"gateway_id","timestamp","dht_temperature","dht_humidity",'
                            '"temperature","luminosity_1","luminosity_2",'
                            '"humidity_1","humidity_2","humidity_3"')
                f.write('\n')
                f.write('"{}",'.format(data.get("plant_id") if data.get("plant_id") is not None else ''))
                f.write('"{}",'.format(data.get("plant_type_name") if data.get("plant_type_name") is not None else ''))
                f.write('"{}",'.format(data.get("creation_date") if data.get("creation_date") is not None else ''))
                f.write('"{}",'.format(data.get("bridge_id") if data.get("bridge_id") is not None else ''))
                f.write('"{}",'.format(data.get("gateway_id") if data.get("gateway_id") is not None else ''))
                f.write('"{}",'.format(data.get("timestamp") if data.get("timestamp") is not None else ''))
                f.write('"{}",'.format(data.get("dht_temperature") if data.get("dht_temperature") is not None else ''))
                f.write('"{}",'.format(data.get("dht_humidity") if data.get("dht_humidity") is not None else ''))
                f.write('"{}",'.format(data.get("temperature") if data.get("temperature") is not None else ''))
                f.write('"{}",'.format(data.get("luminosity_1") if data.get("luminosity_1") is not None else ''))
                f.write('"{}",'.format(data.get("luminosity_2") if data.get("luminosity_2") is not None else ''))
                f.write('"{}",'.format(data.get("humidity_1") if data.get("humidity_1") is not None else ''))
                f.write('"{}",'.format(data.get("humidity_2") if data.get("humidity_2") is not None else ''))
                f.write('"{}",'.format(data.get("humidity_3") if data.get("humidity_3") is not None else ''))
                return
        except FileNotFoundError:
            print('FILE NOT FOUND ERROR in _save_data_to_local_file')
