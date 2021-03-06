################################################################################
# Controllore della comunicazione col database MySQL
# Mette a disposizione delle funzioni per operare sul database
################################################################################

# local
import config as cfg

# standard libraries
import mysql.connector


class DatabaseConnector:

    @property
    def cursor(self):
        return self._cursor

    @property
    def connection(self):
        return self._cnx

    def __init__(self, host=cfg.MYSQL.HOST,
                 user=cfg.MYSQL.USER,
                 passwd=cfg.MYSQL.PASSWORD,
                 database=cfg.MYSQL.DATABASE_NAME):
        print('__init__ called')
        self._host = host
        self._user = user
        self._passwd = passwd
        self._database = database
        self._cnx = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        self._cursor = self._cnx.cursor()
        self.init_tables()

        # self.cursor.execute("CREATE DATABASE progetto_iot")
        # self.cursor.execute("SHOW DATABASES")

    def __del__(self):
        print('__del__ called')
        self._cursor.close()
        if self._cnx.is_connected():
            self._cnx.close()

    def __enter__(self):
        print('__enter__ called')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__ called')
        self._cursor.close()
        if self._cnx.is_connected():
            self._cnx.close()

    def init_tables(self):
        self._cursor.execute("CREATE TABLE IF NOT EXISTS plant_types ("
                             "id INT AUTO_INCREMENT PRIMARY KEY,"
                             "name VARCHAR(255) NOT NULL UNIQUE ,"
                             "description TEXT,"
                             "humidity_min DECIMAL(10,3),"
                             "humidity_max DECIMAL(10,3),"
                             "humidity_tolerance_time INT,"
                             "luminosity_min DECIMAL(10,3),"
                             "luminosity_max DECIMAL(10,3),"
                             "luminosity_tolerance_time INT,"
                             "temperature_min DECIMAL(10,3),"
                             "temperature_max DECIMAL(10,3),"
                             "temperature_tolerance_time INT,"
                             "last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
                             ") ENGINE=INNODB;")

        self._cursor.execute("CREATE TABLE IF NOT EXISTS plants ("
                             "id INT AUTO_INCREMENT PRIMARY KEY,"
                             "last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
                             "plant_id VARCHAR(255) NOT NULL,"
                             "device_id VARCHAR(255) NOT NULL,"
                             "creation_date DATETIME,"
                             "timestamp INT,"
                             "dht_humidity DECIMAL(10,3),"
                             "dht_temperature DECIMAL(10,3),"
                             "luminosity_1 INT,"
                             "luminosity_2 INT,"
                             "humidity_1 INT,"
                             "humidity_2 INT,"
                             "humidity_3 INT,"
                             "temperature DECIMAL(10,3),"
                             "plant_type_id INT,"
                             "CONSTRAINT fk_plant_type_id "
                             "FOREIGN KEY (plant_type_id) "
                             "REFERENCES plant_types(id)"
                             ") ENGINE=INNODB;")

    def insert_plant_data(self, data):
        # expecting "data" formatted as dictionary with keys:
        # - plant_id
        # - device_id
        # - plant_type_id
        # - creation_date
        # - timestamp
        # - dht_humidity, dht_temperature
        # - luminosity_1, luminosity_2
        # - humidity_1, humidity_2, humidity_3
        # - temperature
        assert isinstance(data, dict), 'insert_plant_data(data) - "data" parameter must be a dict'

        self._cursor.execute("INSERT INTO plants (plant_id, device_id, plant_type_id, creation_date,"
                             "timestamp, dht_humidity, dht_temperature, luminosity_1, luminosity_2,"
                             "humidity_1, humidity_2, humidity_3, temperature) "
                             "VALUES (%(plant_id)s, %(device_id)s, %(plant_type_id)s, %(creation_date)s,"
                             "%(timestamp)s, %(dht_humidity)s, %(dht_temperature)s, %(luminosity_1)s, %(luminosity_2)s,"
                             "%(humidity_1)s, %(humidity_2)s, %(humidity_3)s, %(temperature)s)", data)
        self._cnx.commit()
        return self._cursor.lastrowid

    def insert_plant_type_data(self, data):
        # expecting "data" formatted as dictionary with keys:
        # - name
        # - description
        # - humidity_min
        # - humidity_max
        # - humidity_tolerance_time
        # - luminosity_min
        # - luminosity_max
        # - luminosity_tolerance_time
        # - temperature_min
        # - temperature_max
        # - temperature_tolerance_time
        assert isinstance(data, dict), 'insert_plant_type_data(data) - "data" parameter must be a dict'

        self._cursor.execute("INSERT INTO plant_types (name, description, humidity_min, humidity_max,"
                             "humidity_tolerance_time, luminosity_min, luminosity_max, luminosity_tolerance_time,"
                             "temperature_min, temperature_max, temperature_tolerance_time) "
                             "VALUES (%(name)s, %(description)s, %(humidity_min)s, %(humidity_max)s,"
                             "%(humidity_tolerance_time)s, %(luminosity_min)s, %(luminosity_max)s,"
                             "%(luminosity_tolerance_time)s, %(temperature_min)s, %(temperature_max)s,"
                             "%(temperature_tolerance_time)s)", data)
        self._cnx.commit()
        return self._cursor.lastrowid

    # def select_plant_type_by_name(self, name):
    #     self._cursor.execute("SELECT id, name, description, humidity_min, humidity_max, humidity_tolerance_time,"
    #                          "luminosity_min, luminosity_max, luminosity_tolerance_time, temperature_min,"
    #                          "temperature_max, temperature_tolerance_time, last_modified "
    #                          "FROM plant_types "
    #                          "WHERE name = %s", (name,))
    #     return self._cursor.fetchone()

    def select_plant_type_by_name(self, name):
        self._cursor.execute("SELECT * FROM plant_types "
                             "WHERE name = %s", (name,))
        return self._cursor.fetchone()

    def select_plant_by_id(self, plant_id, size=None):
        self._cursor.execute("SELECT * FROM plants "
                             "WHERE plant_id = %s", (plant_id,))
        if size is None:
            return self._cursor.fetchall()
        return self._cursor.fetchmany(size)



