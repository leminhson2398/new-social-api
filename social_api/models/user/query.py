from graphene import ObjectType, Field, String, List, NonNull, Int
from .model import UserType, UserTable
import typing
from social_api.db.common import fetch_one_record_filter_by_one_field, fetch_multiple_records
from graphql.execution.base import ResolveInfo


class Query(ObjectType):
    user_by_email: Field = Field(
        UserType,
        required=False,
        email=String(required=True),
    )

    users: NonNull = NonNull(
        List(UserType, required=False),
        offset=Int(required=False)
    )

    async def resolve_user_by_email(self, info: ResolveInfo, **kwargs) -> typing.Union[None, UserType]:
        userData: typing.Union[None, UserType] = None
        result: typing.Union[typing.Mapping, None] = None

        email: str = kwargs.get('email', '').strip()
        if bool(email):
            # fetch one user based on the provided email:
            result = await fetch_one_record_filter_by_one_field(
                table=UserTable, filterField='email', filterValue=email
            )

        if not result is None:
            userData = dict(result)
            # remove password before sending to next operation
            userData.pop('hashed_password')

        return userData

    async def resolve_users(self, info: ResolveInfo, **kwargs) -> typing.Union[List, typing.List[UserType]]:
        users: list = []
        offset: int = kwargs.get('offset', 0)

        fetchResult: typing.Union[None, typing.List[typing.Mapping]] = await fetch_multiple_records(
            table=UserTable, offset=offset)

        if not fetchResult is None:
            for result in fetchResult:
                userData: typing.Mapping[str, typing.Any] = dict(result)
                # remove 'hashed_password' field first:
                userData.pop('hashed_password')
                users.append(userData)

        return users
