from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.routing import Route
import typing
from graphene import Schema
from .graphql import CustomGraphqlApp, Query, Mutation
from .models import database


allowed_origins: typing.List[str] = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

allowed_methods: typing.List[str] = [
    'POST',
    'GET',
    'OPTIONS'
]

routes: typing.List[Route] = [
    Route(
        '/',
        CustomGraphqlApp(
            schema=Schema(query=Query, mutation=Mutation),
            executor_class=AsyncioExecutor
        )
    )
]


middlewares: typing.List[Middleware] = [
    Middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=allowed_methods
    )
]

app: Starlette = Starlette(routes=routes, middleware=middlewares)


@app.on_event('startup')
async def startup() -> None:
    print('connecting the database')
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    print('disconnecting the database')
    await database.disconnect()
