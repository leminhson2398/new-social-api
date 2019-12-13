from graphene import ObjectType, Field, String
from .model import User, UserType
from ..base import database
from typing import Union
from sqlalchemy import select
from .utils import fetch_user_with_field


class Query(ObjectType):
    user = Field(
        UserType,
        required=True,
        email=String(required=True)
    )

    async def resolve_user(self, info, **kwargs):
        email: Union[str, None] = kwargs.get('email', None)

        result = await fetch_user_with_field(email)

        print(result)
