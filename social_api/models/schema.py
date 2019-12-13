from .user.schema import UserQuery, UserMutation
from .sample.schema import SampleMutation, SampleQuery


class Mutation(
    UserMutation,
    SampleMutation
):
    pass


class Query(
    UserQuery,
    SampleQuery
):
    pass
