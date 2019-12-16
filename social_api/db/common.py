from sqlalchemy import select
import typing
from sqlalchemy import Table
from social_api import config
from databases import Database
from sqlalchemy.sql.selectable import Select


DB_URL: str = config.get('DATABASE_URL', cast=str)

database: Database = Database(DB_URL)


async def fetch_one_record_with_one_field(
    table: Table = None, filterField: str = '', filterValue: typing.Any = None
) -> typing.Union[None, typing.Mapping]:
    """
        fetch at most one record based on provided arguments
        if not found, returns None
    """
    query: Select = select([table]).where(
        table.c[filterField] == filterValue
    )
    return await database.fetch_one(query=query)


async def fetch_multiple_records_with_limit(
    table: Table, filterField: str = '', limit: int = 10, offset: int = 10
) -> typing.Tuple[typing.Mapping]:
    """
        fetch multiple records from table then return them
    """
    pass
