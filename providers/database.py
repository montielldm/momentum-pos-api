from csv import excel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from contextlib import contextmanager

# We load the environment variables
load_dotenv()

USERNAME = os.getenv('USERNAMEDB')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

SQLALCHEMY_STRING_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(
    SQLALCHEMY_STRING_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 20,
        "keepalives_interval": 10,
        "keepalives_count": 3,
    }
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()

def get_session():
    session = SessionLocal()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

class ConnectDatabase:
    __instance = None

    @staticmethod
    def getInstance():
        if ConnectDatabase.__instance is None:
            ConnectDatabase.__instance = ConnectDatabase()
        return ConnectDatabase.__instance

    def __init__(self):
        if ConnectDatabase.__instance is not None:
            raise Exception("ConnectDatabase exists already")
        else:
            self.db = SessionLocal()
