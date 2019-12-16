from .user.schema import UserQuery, UserMutation
from .sample.schema import SampleMutation, SampleQuery
from .file.schema import FileMutation


class Mutation(
    UserMutation,
    SampleMutation,
    FileMutation
):
    pass


class Query(
    UserQuery,
    SampleQuery
):
    pass
