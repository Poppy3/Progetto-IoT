import sqlite3
import time
from IOT_flowey.server import db_config as cfg
import os
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)
        conn.execute(cfg.PRAGMA_JOURNAL_MODE)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_flowey_data(conn, data):
    """
    Insert flowey data into the flowey_data table
    :param conn:
    :param data:
    :return: last row id
    """
    sql = ''' INSERT INTO flowey_data(
				creation_date,
				timestamp,
				dht_temperature,
				dht_humidity,
				temperature,
				luminosity_1,
				luminosity_2)
			  VALUES(
				DATETIME('now','localtime'),
				?,?,?,?,?,?); '''
    cur = conn.cursor()
    cur.execute(sql, data)
    # print("inserting data: ", data)
    # conn.commit()
    return cur.lastrowid


def select_all_flowey_data(conn):
    """
    Query all rows in the flowey_data table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cfg. ORDER BY creation_date DESC")
    rows = cur.fetchall()
    for row in rows:
        # print(row)
        pass
    return rows


def select_last_flowey_data(conn):
    """
    Query last row in the flowey_data table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM flowey_data ORDER BY creation_date DESC LIMIT 1")
    row = cur.fetchone()
    return row


def sql_create_table_statement():
    return """ CREATE TABLE IF NOT EXISTS flowey_data (
				id integer PRIMARY KEY,
				creation_date text NOT NULL,
				timestamp integer NOT NULL,
				dht_temperature real NOT NULL,
				dht_humidity real NOT NULL,
				temperature real NOT NULL,
				luminosity_1 integer NOT NULL,
				luminosity_2 integer NOT NULL,
				humidity_1 integer NOT NULL,
				humidity_2 integer NOT NULL,
				humidity_3 integer NOT NULL
			); """


if __name__ == '__main__':
    """ used only during development """

    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), cfg.DATABASE_NAME)
    print(database_path)

    sql_create_table_flowey_data = sql_create_table_statement()

    # create a database connection
    conn = create_connection(database_path)
    with conn:
        # create flowey_data table
        create_table(conn, cfg.SQL.TABLE_PLANT.STATEMENT_CREATE)

        # create a new row
        flowey_data_vals = (2775, 27.00, 64.00, 26.98, 55, 48)
        row_id = insert_flowey_data(conn, flowey_data_vals)
        time.sleep(1.1)
        flowey_data_vals = (5544, 28.00, 65.00, 27.88, 56, 50)
        row_id = insert_flowey_data(conn, flowey_data_vals)
        select_all_flowey_data(conn)
