class SQL:
    class TABLE_PLANT:
        NAME = "PLANT"
        class COLUMNS:
            PLANT_ID: "PLANT_ID"
            CREATION_DATE: "CREATION_DATE"
            TIMESTAMP: "TIMESTAMP"
            DHT_TEMPERATURE: "DHT_TEMPERATURE"
            DHT_HUMIDITY: "DHT_HUMIDITY"
            TEMPERATURE: "TEMPERATURE"
            LUMINOSITY_1: "LUMINOSITY_1"
            LUMINOSITY_2: "LUMINOSITY_2"
            HUMIDITY_1: "HUMIDITY_1"
            HUMIDITY_2: "HUMIDITY_2"
            HUMIDITY_3: "HUMIDITY_3"
        STATEMENT_CREATE = """
            CREATE TABLE IF NOT EXISTS PLANT (
                ID integer PRIMARY KEY,
                PLANT_ID text NOT NULL,
                CREATION_DATE text NOT NULL,
                TIMESTAMP integer,
                DHT_TEMPERATURE real,
                DHT_HUMIDITY real,
                TEMPERATURE real,
                LUMINOSITY_1 integer,
                LUMINOSITY_2 integer,
                HUMIDITY_1 integer,
                HUMIDITY_2 integer,
                HUMIDITY_3 integer
            ); """
        STATEMENT_INSERT = """
            INSERT INTO PLANT(
                PLANT_ID,
                CREATION_DATE,
                TIMESTAMP,
                DHT_TEMPERATURE,
                DHT_HUMIDITY,
                TEMPERATURE,
                LUMINOSITY_1,
                LUMINOSITY_2,
                HUMIDITY_1,
                HUMIDITY_2,
                HUMIDITY_3)
			VALUES(
				DATETIME('now','localtime'),
				?,?,?,?,?,?); """

PRAGMA_JOURNAL_MODE = "pragma journal_mode=wal"

DATABASE_NAME = "database.db"
