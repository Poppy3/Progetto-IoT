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
DB_WRITE_DELAY = 60.0  # delay in secondi tra una scrittura sul db e l'altra


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
		"- /flowey : mostra i dati provenienti dal canale seriale di arduino\n"
		)
	))


def show_flowey(chat_id):
	conn = sql.create_connection(DATABASE_NAME)
	text = "Niente da fare :("
	with conn:
		text = sql.select_last_flowey_data(conn)
	send_message(prepare_response(chat_id, text))


def setup_db():
	database = r'C:\Users\damia\Desktop\flowey.db'
	sql_create_table_flowey_data = """ CREATE TABLE IF NOT EXISTS flowey_data (
										id integer PRIMARY KEY,
										creation_date text NOT NULL,
										timestamp integer NOT NULL,
										dht_temperature real NOT NULL,
										dht_humidity real NOT NULL,
										temperature real NOT NULL,
										luminosity_1 integer NOT NULL,
										luminosity_2 integer NOT NULL
									); """
	# create a database connection
	conn = sql.create_connection(DATABASE_NAME)
	with conn:
		# create flowey_data table
		sql.create_table(conn, sql_create_table_flowey_data)
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


def run_bottle():
	print("Avviato run_bottle")
	run(host='localhost', port=8080, debug=True)


def run_flowey_db_writer():
	print("Avviato run_flowey_db_writer")
	flowey = FloweyArduino()
	conn = setup_db()
	last_time = time.time()
	with conn:
		while True:
			try:
				data = flowey.readline()
				if data is not None:
					sql_data = (data['timestamp'],
								data['dht_temperature'],
								data['dht_humidity'],
								data['temperature'],
								data['luminosity_1'],
								data['luminosity_2'])
					if time.time() - last_time > DB_WRITE_DELAY:
						sql.insert_flowey_data(conn, sql_data)
						print("tick: ", time.time())
						last_time = time.time()
			except:
				print("Received Interrupt -> breaking from while True")
				break


if __name__ == '__main__':
	try:
		bot = mp.Process(target=run_bottle)
		flowey_db_writer = mp.Process(target=run_flowey_db_writer)
		bot.start()
		flowey_db_writer.start()
	except:
		bot.close()
		flowey_db_writer.close()
