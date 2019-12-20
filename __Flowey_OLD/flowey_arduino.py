import json
import serial
import time

class FloweyArduino:
	# serial parameters
	# SERIAL_PORT = 'COM3'
	# SERIAL_NUM = 9600

	def __init__(self, serial_port='COM3', serial_num=9600):
		self._serial_port = serial_port
		self._serial_num = serial_num
		self._ser = serial.Serial(serial_port, serial_num)
		self._status_code = 0

	def readline(self):
		""" expecting this format from the serial channel of the arduino
		{
			"UUID": "ARDUINO001",
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
		for i in range(10):  # max 10 tentatives
			s = self._ser.readline()  # as binary
			if s is not None:
				try:  # first line of serial may be not complete
					js = json.loads(s.decode())
					return js
				except:
					time.sleep(0.33)
			time.sleep(2)
		return None

	def close(self):
		self._ser.close()

	def control_led_OK_GREEN(self):
		self._status_code = 0
		self._ser.write(b'0')

	def control_led_WARNING_YELLOW(self):
		self._status_code = 1
		self._ser.write(b'1')

	def control_led_WARNING_ORANGE(self):
		self._status_code = 2
		self._ser.write(b'2')

	def control_led_ALERT_RED(self):
		self._status_code = 3
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
