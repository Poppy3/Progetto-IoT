################################################################################
# DEVELOPMENT file usato per testare le
# funzioni contenute in 'database_connector.py'
################################################################################

# local
from database_connector import DatabaseConnector

# standard libraries
# - none -

if __name__ == '__main__':
    cnx = DatabaseConnector()

    plant_type_name = 'cactus'

    plant_type_data = {
        'plant_type_name': plant_type_name,
        # TODO
    }

    plant_data = {
        # TODO
    }

    plant_type_id = cnx.insert_plant_type_data(plant_type_data)

    plant_data["plant_type_id"] = plant_type_id

    cnx.insert_plant_data(plant_data)

    print(cnx.select_plant_type_by_name(plant_type_name))

    # TODO testa la roba se funziona

