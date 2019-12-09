from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine
from databases import Database
from social_api import config


DB_URL: str = config.get('DATABASE_URL', cast=str)

STD_NUMBER_OF_RESULT_AT_A_TIME: int = 10

# sqlalchemy model base
Base = declarative_base()

# create database:
database: Database = Database(DB_URL)

# create engine:
engine = create_engine(DB_URL)

# create metadata:
metadata: MetaData = MetaData()

# create tables:
Base.metadata.create_all(engine)

