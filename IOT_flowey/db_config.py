SQL_CREATE_TABLE_PLANT = """
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

PRAGMA_JOURNAL_MODE = "pragma journal_mode=wal"
DATABASE_NAME = "database.db"