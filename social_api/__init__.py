from starlette.config import Config
import logging
import sys
from os import path
from sqlalchemy import create_engine, MetaData
from databases import Database

CURDIR: str = path.dirname(
    path.abspath(__file__)
)

# append for import
sys.path.append("..")

# configure logging:
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.ERROR
)

config: Config = Config(
    path.join(CURDIR, ".env")
)

# metadata:
metadata: MetaData = MetaData()

# create database:
database: Database = Database(config.get('DATABASE_URL', None))

# create engine:
engine = create_engine(
    config.get('DATABASE_URL'),
)

# if not metadata.is_bound():
#     metadata.create_all(bind=engine)
