from graphene import ObjectType, Field, String, List, NonNull
from .model import User, UserType
from ..base import database
import typing
from .utils import fetch_user_with_field
from ..base import STD_NUMBER_OF_RESULT_AT_A_TIME
from graphql.execution.base import ResolveInfo


def func():
    import time

    time.sleep(5)
    print('done sleep')


class Query(ObjectType):
    user_by_email: Field = Field(
        UserType,
        required=False,
        email=String(required=True),
    )

    users: NonNull = NonNull(
        List(UserType, required=False)
    )

    async def resolve_user_by_email(self, info: ResolveInfo, **kwargs) -> typing.Union[None, UserType]:
        userData: typing.Union[None, UserType] = None
        result: typing.Union[typing.Mapping, None] = None

        email: str = kwargs.get('email', '').strip()
        if bool(email):
            result = await fetch_user_with_field(email=email)

        if not result is None:
            userData = dict(result)
            userData.pop('hashed_password')

        background = info.context['background']
        background.add_task(func)
        return userData

    async def resolve_users(self, info, **kwargs) -> typing.Union[List, typing.List[UserType]]:
        pass
