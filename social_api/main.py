from social_api.db.base import database
from fastapi import FastAPI
from social_api.graphql.graphql import CustomGraphqlApp
from graphene import Schema
from social_api.models.schema import Query, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from social_api.middleware.auth import AuthBackend
from .import settings


app = FastAPI()


app.add_route(
    path='/',
    route=CustomGraphqlApp(
        schema=Schema(query=Query, mutation=Mutation),
        executor_class=AsyncioExecutor
    )
)

# add middlewares:
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# add authentication middleware
app.add_middleware(
    AuthenticationMiddleware,
    backend=AuthBackend()
)


@app.on_event('startup')
async def startup() -> None:
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    await database.disconnect()
