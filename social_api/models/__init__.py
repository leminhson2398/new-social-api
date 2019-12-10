from sqlalchemy import MetaData, create_engine
from databases import Database
from social_api import config
from .base import Base
from .user import User
from .file import UserPicture


DB_URL: str = config.get('DATABASE_URL', cast=str)

STD_NUMBER_OF_RESULT_AT_A_TIME: int = 10


# create database:
database: Database = Database(DB_URL)

# create engine:
engine = create_engine(DB_URL)

# create metadata:
metadata: MetaData = MetaData()

# create tables:
Base.metadata.create_all(engine)
