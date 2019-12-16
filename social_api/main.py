from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Route
from .graphql import CustomGraphqlApp
import typing
from graphene import Schema
from .models.schema import Query, Mutation
from .models.base import database
from .middleware.auth import AuthBackend


# add allowed origins
allowed_origins: typing.List[str] = [
    # 'http://localhost:3000',
    # 'http://127.0.0.1:3000',
    # 'localhost',
    # '127.0.0.1',
    # 'http://localhost',
    # 'http://127.0.0.1'
    '*'
]

# add allowed hosts
allowed_methods: typing.List[str] = [
    'POST',
    'GET',
    'OPTIONS'
]

# main route for app
routes: typing.List[Route] = [
    Route(
        '/',
        CustomGraphqlApp(
            schema=Schema(query=Query, mutation=Mutation),
            executor_class=AsyncioExecutor
        )
    )
]

# specify middlewares
middlewares: typing.List[Middleware] = [
    Middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        # allow_credentials=True,
        allow_methods=allowed_methods
    ),
    Middleware(
        AuthenticationMiddleware,
        backend=AuthBackend()
    ),
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_origins
    )
]

# init starlette app:
app: Starlette = Starlette(routes=routes, middleware=middlewares)


@app.on_event('startup')
async def startup() -> None:
    print('connecting the database')
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    print('disconnecting the database')
    await database.disconnect()
