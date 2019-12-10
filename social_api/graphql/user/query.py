from graphene import (
    ObjectType,
    Field,
    Int
)
from .graphql_type import UserType
import typing
from ...models import database
from ...models.user import User


class Query(ObjectType):
    user = Field(
        UserType,
        required=False,
        id=Int(required=True)
    )

    async def resolve_user(self, info, **kwargs):
        id: typing.Union[int, None] = kwargs.get('id', None)
        if id:
            print(type(User))

