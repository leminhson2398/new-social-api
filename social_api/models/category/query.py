from graphene import ObjectType, NonNull, List
from .model import CategoryType, CategoryTable, SubCategoryTable
from graphql.execution.base import ResolveInfo
from social_api.db.base import database
import typing
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql import text


class Query(ObjectType):
    categories = NonNull(
        List(CategoryType, required=False)
    )

    async def resolve_categories(self, info: ResolveInfo, **kwargs):
        allCategories: typing.List[typing.Mapping[str, typing.Any]] = []
        """
        returns all categories and their subs
        """
        # query: Select = select([
        #     CategoryTable,
        #     SubCategoryTable
        # ]).select_from(
        #     CategoryTable.join(right=SubCategoryTable)
        # )
        query: Select = CategoryTable.select()
        # fetchResult: typing.Union[None, typing.List[typing.Mapping]] = await database.fetch_all(query=query)
        async for data in database.iterate(query=query):
            print(dict(data))

        # for d in fetchResult:
        #     print(dict(d))

        return allCategories
