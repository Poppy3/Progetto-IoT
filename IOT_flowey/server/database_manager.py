
# local
import config as cfg

# standard libraries
import mysql.connector

mydb = mysql.connector.connect(
    host=cfg.MYSQL.HOST,
    user=cfg.MYSQL.USER,
    passwd=cfg.MYSQL.PASSWORD,
    database=cfg.MYSQL.DATABASE_NAME,
)

cursor = mydb.cursor()

#cursor.execute("CREATE DATABASE progetto_iot")
#cursor.execute("SHOW DATABASES")

cursor.execute("CREATE TABLE IF NOT EXISTS plant_types ("
               "id INT AUTO_INCREMENT PRIMARY KEY,"
               "name VARCHAR(255) NOT NULL,"
               "description TEXT,"
               "humidity_min DECIMAL,"
               "humidity_max DECIMAL,"
               "humidity_tolerance_time INT,"
               "luminosity_min DECIMAL,"
               "luminosity_max DECIMAL,"
               "luminosity_tolerance_time INT,"
               "temperature_min DECIMAL,"
               "temperature_max DECIMAL,"
               "temperature_tolerance_time INT,"
               "last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
               ") ENGINE=INNODB;")

cursor.execute("CREATE TABLE IF NOT EXISTS plants ("
               "id INT AUTO_INCREMENT PRIMARY KEY,"
               "last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
               "plant_id VARCHAR(255) NOT NULL,"
               "device_id VARCHAR(255) NOT NULL,"
               "creation_date DATETIME,"
               "timestamp INT,"
               "dht_humidity DECIMAL,"
               "dht_temperature DECIMAL,"
               "luminosity_1 INT,"
               "luminosity_2 INT,"
               "humidity_1 INT,"
               "humidity_2 INT,"
               "humidity_3 INT,"
               "temperature DECIMAL,"
               "plant_type_id INT,"
               "CONSTRAINT fk_plant_type_id "
               "FOREIGN KEY (plant_type_id) "
               "REFERENCES plant_types(id)"
               ") ENGINE=INNODB;")


