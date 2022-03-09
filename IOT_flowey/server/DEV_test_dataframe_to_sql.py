import pandas as pd
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, DateTime, BigInteger
import sqlalchemy as db
import os
from dataclasses import dataclass
from datetime import datetime

DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flowey_dev.sqlite3')
HOSTED_APP_URL = 'https://iotproject.eu.pythonanywhere.com'
API_PLANT_DATA = '/api/v1/plant_data'
API_PLANT_TYPE = '/api/v1/plant_type'

Base = declarative_base()


@dataclass
class PlantTypeModel(Base):
    __tablename__ = 'plant_type'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    last_modified: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name: str = Column(String(length=128), nullable=False, unique=True)
    description: str = Column(Text)
    humidity_min: float = Column(Float)
    humidity_max: float = Column(Float)
    humidity_tolerance_time: int = Column(Integer)
    luminosity_min: float = Column(Float)
    luminosity_max: float = Column(Float)
    luminosity_tolerance_time: int = Column(Integer)
    temperature_min: float = Column(Float)
    temperature_max: float = Column(Float)
    temperature_tolerance_time: int = Column(Integer)

    plant_data = relationship('PlantDataModel',
                              # backref='plant_type',
                              lazy=True)


@dataclass()
class PlantDataModel(Base):
    __tablename__ = 'plant_data'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    last_modified: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    plant_id: str = Column(String(length=50), nullable=False)
    bridge_id: str = Column(String(length=50), nullable=False)
    gateway_id: str = Column(String(length=50), nullable=False)
    creation_date: datetime = Column(DateTime)
    timestamp: int = Column(BigInteger)
    dht_humidity: float = Column(Float)
    dht_temperature: float = Column(Float)
    luminosity_1: int = Column(Integer)
    luminosity_2: int = Column(Integer)
    humidity_1: int = Column(Integer)
    humidity_2: int = Column(Integer)
    humidity_3: int = Column(Integer)
    temperature: float = Column(Float)

    plant_type_id: int = Column(Integer, ForeignKey('plant_type.id'), nullable=False)


if __name__ == '__main__':
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_json(HOSTED_APP_URL + API_PLANT_DATA)
    df.to_json('plant_data.json')
    # df = pd.read_json('plant_data.json')

    df_trimmed = df[(df['creation_date'] > '2021-05-09') & (df['creation_date'] < '2021-08-03')]
    df_trimmed.to_json('plant_data__trimmed.json')

    dft = pd.read_json(HOSTED_APP_URL + API_PLANT_TYPE)
    dft.to_json('plant_type.json')
    # dft = pd.read_json('plant_type.json')

    engine = db.create_engine(DATABASE_URI)
    df_trimmed.to_sql(name='plant_data', con=engine, index=False)
    dft.to_sql(name='plant_type', con=engine, index=False)


