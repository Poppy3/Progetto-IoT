################################################################################
# DEVELOPMENT file usato per testare le funzioni relative all'interazione tra
# Pandas e MySql. Serviranno per utilizzare facebook-prophet coi dati presenti
# nel database
################################################################################

# local
from database_connector import DatabaseConnector

# standard libraries
import pandas as pd


if __name__ == '__main__':
    with DatabaseConnector() as cnx:
        df = pd.read_sql("select * from plants", cnx.connection)
        print(df.head())
    print('finished')
