from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from geoalchemy2 import Geography
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class ChargingStation(Base):

    __tablename__ = "ev_stations"

    id = Column(Integer, primary_key=True, index=True)

    station_name = Column(Text)
    address = Column(Text)
    city = Column(Text)
    state = Column(Text)

    latitude = Column(Float)
    longitude = Column(Float)

    operator = Column(Text)
    charger_type = Column(Text)
    connector_type = Column(Text)

    power_kw = Column(Float)

    access_type = Column(Text)
    opening_hours = Column(Text)
    contact_phone = Column(Text)

    source = Column(Text)

    location = Column(Geography("POINT", srid=4326))



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
