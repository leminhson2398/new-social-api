from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    BaseUser
)
import jwt
from social_api import config
from ..models.user.model import UserTable
import logging
from starlette.requests import Request
import typing
from social_api.db.common import fetch_one_record_filter_by_one_field
from sqlalchemy import select, and_


class CustomAuthenticatedUser(SimpleUser):
    def __init__(self, id: int, username: str) -> None:
        self.id: typing.Union[int, str] = id
        super(CustomAuthenticatedUser, self).__init__(username=username)


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: Request) -> typing.Tuple[AuthCredentials, BaseUser]:
        auth: str = conn.headers.get('Authorization', default='')
        if bool(auth):
            # auth in form of: 'JWT kjdfkldjfoirtjig'.
            scheme, credentials = auth.split(sep=' ', maxsplit=1)
            if scheme.lower() != 'jwt':
                return
            try:
                decoded: typing.Mapping[str, typing.Any] = jwt.decode(
                    jwt=credentials,
                    key=config.get('SECRET', default=''),
                    verify=True,
                    algorithms=['HS256']
                )
            except jwt.PyJWTError as e:
                logging.error(f"Error decoding authorization: {e}.")
                return
            # decoded looks like this:
            """
            {'username': value, 'id': value, 'expire': value}
            """
            username, userId, expire = [
                decoded.get(key, None) for key in ['username', 'id', 'expire']
            ]
            if not all(bool(i) for i in [id, username, expire]):
                raise AuthenticationError('Invalid token')
            else:
                userById: typing.Union[typing.Mapping, None] = await fetch_one_record_filter_by_one_field(
                    table=UserTable,
                    filterField='id',
                    filterValue=userId
                )
                if not userById is None:
                    # user does exist:
                    return (
                        AuthCredentials(['authenticated']),
                        CustomAuthenticatedUser(
                            id=userId,
                            username=username
                        ),
                    )
                else:
                    return
        else:
            return
