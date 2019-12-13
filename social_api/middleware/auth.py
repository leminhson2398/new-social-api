from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser
)
import jwt
from ..models.base import config
from ..models.user.model import User
import logging
from starlette.requests import HTTPConnection
import typing
from starlette.datastructures import Headers
from ..models.base import database
# from sqlalchemy.engine.result import ResultProxy
from sqlalchemy import select, and_


class CustomAuthenticatedUser(object):
    def __init__(self, id: int, username: str) -> None:
        self.id: str = id
        self.username: str = username

    @property
    def is_authenticated(self) -> bool:
        return True


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> typing.Union[
        typing.List(AuthCredentials, CustomAuthenticatedUser), None
    ]:
        auth: str = conn.headers.get('Authentication', default='')
        if bool(auth):
            # auth in form of: 'JWT kjdfkldjfoirtjig'.
            scheme, credentials = auth.split(' ', maxsplit=1)
            if scheme.lower() != 'jwt':
                return None
            try:
                decoded: typing.Mapping[str, typing.Any] = jwt.decode(
                    credentials, config.get('SECRET', default=''),
                    algorithms=['HS256']
                )
            except jwt.PyJWTError as e:
                logging.error(f"Error decoding authorization: {e}.")
                return None
            """
            decoded has form of: {'username': value, 'id': value, 'expire': value}
            """
            if not all([bool(decoded.get(key, None)) for key in ['username', 'id', 'expire']]):
                raise AuthenticationError('Invalid token')
            else:
                userTable = User.__table__
                query: typing.Any = select([userTable]).where(
                    and_(
                        userTable.c.username == decoded['username'],
                        userTable.c.id == decoded['id'],
                    )
                )
                user: typing.Mapping = await database.fetch_one(query=query)
                if user:
                    # user does exist:
                    return (
                        AuthCredentials(['authenticated']),
                        CustomAuthenticatedUser(
                            id=decoded['id'],
                            username=decoded['username']
                        ),
                    )
                else:
                    return None
        else:
            return None
