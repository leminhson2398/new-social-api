from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from sqlalchemy import create_engine, MetaData
from social_api import config


DB_URL: str = config.get('DATABASE_URL', cast=str)


# create engine:
engine = create_engine(DB_URL)

# create metadata:
metadata: MetaData = MetaData()

# create database:
database: Database = Database(DB_URL)

# create model Base:
Base = declarative_base()

STD_NUMBER_OF_RESULT_AT_A_TIME: int = 10
