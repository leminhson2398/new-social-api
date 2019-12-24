from graphene import ObjectType, NonNull, List
from .model import CategoryGroupType, CategoryGroupTable, CategoryTable, CategoryType
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
        query: Select = select([
            CategoryTable
        ])

        print(query)

        result = await database.fetch_all(query=query)
        for row in result:
            print(dict(row))

        # for d in fetchResult:
        #     print(dict(d))

        return allCategories
