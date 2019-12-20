import json
import os
import multiprocessing as mp
import requests
import serial
import time
from flowey_arduino import FloweyArduino
import sqlite_manager as sql
from bottle import (  
	run, post, response, request as bottle_request
)


# <--- add your telegram token here; it should be like https://api.telegram.org/bot12345678:SOMErAn2dom/
BOT_URL = 'https://api.telegram.org/bot744755426:AAHCNYYTctEwvwW_PBzBK7NV8fh1pHkqaiQ/'
DATABASE_NAME = r'C:\Users\damia\Desktop\flowey.db'
DB_WRITE_DELAY = 0.0  # delay in secondi tra una scrittura sul db e l'altra


def send_message(prepared_data):  
	"""
	Prepared data should be json which includes at least `chat_id` and `text`
	""" 
	message_url = BOT_URL + 'sendMessage'
	requests.post(message_url, json=prepared_data)


def prepare_response(chat_id, text):  
	return {
		"chat_id": chat_id,
		"text": text,
	}


def get_chat_id(data):  
	"""
	Method to extract chat id from telegram request.
	"""
	return data['message']['chat']['id']


def get_message(data):  
	"""
	Method to extract message id from telegram request.
	"""
	return data['message']['text']


def show_help(chat_id):
	send_message(prepare_response(chat_id,
		(
		"I comandi disponibili sono:\n"
		"- /help : mostra questo messaggio\n"
		"- /flowey : mostra l'ultima riga scritta sul db\n"
		)
	))


def show_flowey(chat_id):
	conn = sql.create_connection(DATABASE_NAME)
	text = "Niente da fare :("
	with conn:
		text = sql.select_last_flowey_data(conn)
	send_message(prepare_response(chat_id, text))


def setup_db():
	conn = sql.create_connection(DATABASE_NAME)
	with conn:
		sql.create_table(conn, sql.sql_create_table_statement())
		return conn
	return None


@post('/')
def main():  
	data = bottle_request.json
	#print("received data:\n", data)	

	chat_id = get_chat_id(data)
	msg = get_message(data)
	if msg == '/help' or msg == '/start':
		show_help(chat_id)
	elif msg == '/flowey':
		show_flowey(chat_id)
	else:
		pass

	return response  # status 200 OK by default


def run_bottle_server():
	print("Avviato run_bottle_server")
	run(host='localhost', port=8080, debug=True)


def run_flowey():
	print("Avviato run_flowey")
	flowey = FloweyArduino()
	conn = setup_db()
	last_time = time.time()
	
	increase = True
	
	with conn:
		while True:
			try:
				data = flowey.readline()
				if data is not None:
					print("Serial data received: ", data)
					sql_data = (data['UUID'],
								data['timestamp'],
								data['dht_temperature'],
								data['dht_humidity'],
								data['temperature'],
								data['luminosity_1'],
								data['luminosity_2'],
								data['humidity_1'],
								data['humidity_2'],
								data['humidity_3']
								)
					# CODICE TEMPORANEO QUA, per provare il led comandato col seriale
					print("IN: flowy status: ", flowey._status_code)
					if increase:
						flowey.increase_severity_level()
						if flowey._status_code == 3:
							increase = False
					else:
						flowey.decrease_severity_level()
						if flowey._status_code == 0:
							increase = True
					print("OU: flowy status: ", flowey._status_code)
					# eo CODICE TEMPORANEO QUA, per provare il led comandato col seriale
					
					if DB_WRITE_DELAY > 0:
						if time.time() - last_time > DB_WRITE_DELAY:
							sql.insert_flowey_data(conn, sql_data)
							print("tick: ", time.time())
							last_time = time.time()
			except:
				print("Received Interrupt -> breaking from while True")
				break


if __name__ == '__main__':
	try:
		server_proc = mp.Process(target=run_bottle_server)
		flowey_proc = mp.Process(target=run_flowey)
		server_proc.start()
		flowey_proc.start()
	except:
		server_proc.close()
		flowey_proc.close()
