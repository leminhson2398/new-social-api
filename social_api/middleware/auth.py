from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    BaseUser
)
import jwt
from ..models.base import config
from ..models.user.model import UserTable
import logging
from starlette.requests import Request
import typing
from starlette.datastructures import Headers
from ..models.base import database
from sqlalchemy import select, and_


class CustomAuthenticatedUser(SimpleUser):
    def __init__(self, id: int, username: str) -> None:
        self.id: typing.Union[int, str] = id
        super(CustomAuthenticatedUser, self).__init__(username=username)


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: Request) -> typing.Tuple[AuthCredentials, BaseUser]:
        auth: str = conn.headers.get('Authentication', default='')
        if bool(auth):
            # auth in form of: 'JWT kjdfkldjfoirtjig'.
            scheme, credentials = auth.split(sep=' ', maxsplit=1)
            if scheme.lower() != 'jwt':
                return
            try:
                decoded: typing.Mapping[str, typing.Any] = jwt.decode(
                    credentials, config.get('SECRET', default=''),
                    algorithms=['HS256']
                )
            except jwt.PyJWTError as e:
                logging.error(f"Error decoding authorization: {e}.")
                return
            # decoded looks like this:
            """
            {'username': value, 'id': value, 'expire': value}
            """
            username, id, expire = [decoded.get(key, None) for key in [
                'username', 'id', 'expire']]
            if not all(bool(i) for i in [id, username, expire]):
                raise AuthenticationError('Invalid token')
            else:
                query: typing.Any = select([UserTable]).where(
                    and_(
                        UserTable.c.username == username,
                        UserTable.c.id == id,
                    )
                )
                user: typing.Mapping = await database.fetch_one(query=query)
                if user:
                    # user does exist:
                    return (
                        AuthCredentials(['authenticated']),
                        CustomAuthenticatedUser(
                            id=id,
                            username=username
                        ),
                    )
                else:
                    return
        else:
            return
