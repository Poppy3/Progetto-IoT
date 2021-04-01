################################################################################
# Controllore della comunicazione col gateway (=arduino)
# Mette a disposizione delle funzioni per leggere/scrivere da/verso il gateway
################################################################################

# local
import config as cfg
from utils import debug, error, warning

# standard libraries
from serial import Serial, SerialException
import json
import time


class GatewayConnector:
    # default serial parameters
    # SERIAL_PORT = 'COM3'
    # SERIAL_NUM = 9600

    def __init__(self, port='COM3', baudrate=9600, status=0,
                 timeout=cfg.GATEWAY_CONNECTOR.TIMEOUT,
                 local_mode=cfg.GATEWAY_CONNECTOR.LOCAL_MODE):
        self._port = port
        self._baudrate = baudrate
        self._status_code = status
        self._local_mode = local_mode
        self._timeout = timeout
        if self._local_mode is not True:
            self._ser = Serial(port, baudrate, timeout=timeout, exclusive=True)

    def __del__(self):
        self.close()

    def _readline_local(self):
        import random
        sample_data = {
            "gateway_id": "ARDUINO001",
            "timestamp": random.randint(111, 9999),
            "dht_temperature": random.randrange(1, 99),
            "dht_humidity": random.randrange(1, 99),
            "temperature": random.randrange(1, 99),
            "luminosity_1": random.randint(1, 99),
            "luminosity_2": random.randint(1, 99),
            "humidity_1": random.randint(1, 99),
            "humidity_2": random.randint(1, 99),
            "humidity_3": random.randint(1, 99)
        }
        time.sleep(cfg.GATEWAY_CONNECTOR.READ_INTERVAL_TIME)
        return sample_data

    def readline(self):
        """ expecting this data format from the serial channel of the arduino
        {
            "device_id": "ARDUINO001",
            "timestamp" : 1234,
            "dht_temperature" : 12.34,
            "dht_humidity" : 12.34,
            "temperature" : 12.34,
            "luminosity_1" : 1234,
            "luminosity_2" : 1234,
            "humidity_1" : 1234,
            "humidity_2" : 1234,
            "humidity_3" : 1234
        }
        """
        debug('called readline', 2)
        # TODO - dopo aver collegato l'arduino, si può rimuovere questo blocco
        if self._local_mode:
            return self._readline_local()

        max_tries = cfg.GATEWAY_CONNECTOR.READ_MAX_TRIES
        for ith_try in range(max_tries):  # max tentatives
            try:
                while True:
                    if self._ser.in_waiting > 0:
                        debug(f'Serial data incoming: {self._ser.in_waiting} bytes', 2)
                        try:
                            line = self._ser.readline()
                            debug(f'Received serial data: {line}', 2)
                            js = json.loads(line.decode())
                            return js
                        except ValueError as e:
                            error(f'gateway readline() got ValueError: {e}')
                        except SerialException as e:
                            error(f'gateway readline() got SerialException: {e}')
                        except OSError as e:
                            error(f'gateway _ser.readline() got OSError: {e}')
                        except Exception as e:
                            error(f'gateway readline() encountered unexpected {type(e)}: {e}')
                        finally:
                            break
            except OSError as e:
                error(f'gateway readline() got OSError: {e}')
            warning(f'Problems while reading serial data. '
                    f'Reopening serial connection and retrying... (Try #{ith_try} of {max_tries})')
            self.reopen()
            time.sleep(cfg.GATEWAY_CONNECTOR.READ_INTERVAL_TIME)
        # exceeded max tries without reading
        return None

    def open(self):
        if not self._local_mode:
            self._ser.open()

    def close(self):
        if not self._local_mode:
            self._ser.close()

    def reopen(self):
        self.close()
        self.open()

    def control_led_OK_GREEN(self):
        debug('control_led_OK_GREEN - status_code = 0', 2)
        self._status_code = 0
        if not self._local_mode:
            self._ser.write(b'0')

    def control_led_WARNING_YELLOW(self):
        debug('control_led_WARNING_YELLOW - status_code = 1', 2)
        self._status_code = 1
        if not self._local_mode:
            self._ser.write(b'1')

    def control_led_WARNING_ORANGE(self):
        debug('control_led_WARNING_ORANGE - status_code = 2', 2)
        self._status_code = 2
        if not self._local_mode:
            self._ser.write(b'2')

    def control_led_ALERT_RED(self):
        debug('control_led_ALERT_RED - status_code = 3', 2)
        self._status_code = 3
        if not self._local_mode:
            self._ser.write(b'3')

    def increase_severity_level(self):
        if self._status_code == 0:
            self.control_led_WARNING_YELLOW()
        elif self._status_code == 1:
            self.control_led_WARNING_ORANGE()
        elif self._status_code >= 2:
            self.control_led_ALERT_RED()

    def decrease_severity_level(self):
        if self._status_code <= 1:
            self.control_led_OK_GREEN()
        elif self._status_code == 2:
            self.control_led_WARNING_YELLOW()
        elif self._status_code == 3:
            self.control_led_WARNING_ORANGE()
