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

	def readline(self):
		""" expecting this format from the serial channel of the arduino
		{
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
