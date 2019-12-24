from databases import Database
from social_api import config
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import create_engine


DB_URL: str = config.get('DATABASE_URL', cast=str)

# init database:
database: Database = Database(DB_URL)

# init engine:
engine = create_engine(DB_URL)

# init Base:
Base: DeclarativeMeta = declarative_base()

STD_NUMBER_OF_RESULT_AT_A_TIME: int = 10
