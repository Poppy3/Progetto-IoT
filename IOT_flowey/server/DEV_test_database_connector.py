################################################################################
# DEVELOPMENT file usato per testare le
# funzioni contenute in 'database_connector.py'
################################################################################

# local
from database_connector import DatabaseConnector

# standard libraries
import datetime

if __name__ == '__main__':
    cnx = DatabaseConnector()

    datetime_now = datetime.datetime.now()
    plant_type_name = f'cactus {datetime_now.strftime("%H%M%S")}'

    # data to be saved in 'plant_types' mysql table
    plant_type_data = {
        'name': plant_type_name,
        'description': 'descrizione lunga della pianta lorem ipsum dir sat amet lorem ipsum dir sat amet lorem ipsum.',
        "humidity_min": 12.34,
        "humidity_max": 98.76,
        "humidity_tolerance_time": 1234,
        "luminosity_min": 12.34,
        "luminosity_max": 98.76,
        "luminosity_tolerance_time": 1234,
        "temperature_min": 12.34,
        "temperature_max": 98.76,
        "temperature_tolerance_time": 1234
    }

    print(f'inserting into plant_types with data:\n{plant_type_data}\n')
    plant_type_id = cnx.insert_plant_type_data(plant_type_data)

    # data to be saved in 'plants' mysql table
    plant_data = {"plant_id": "FAKE_PLANT001", "device_id": "FAKE_ARDUINO001", "creation_date": datetime_now,
                  "timestamp": 12345678, "dht_temperature": 12.34, "dht_humidity": 12.34, "temperature": 12.34,
                  "luminosity_1": 1234, "luminosity_2": 1234, "humidity_1": 1234, "humidity_2": 1234,
                  "humidity_3": 1234, "plant_type_id": plant_type_id}

    print(f'inserting into plants with data:\n{plant_data}\n')
    cnx.insert_plant_data(plant_data)

    # trying a SELECT statement
    result = cnx.select_plant_type_by_name(plant_type_name)
    print(f'result from select_plant_type_by_name({plant_type_name}):\n{result}\n')
