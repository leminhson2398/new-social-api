from .user.schema import UserQuery, UserMutation
from .sample.schema import SampleMutation, SampleQuery
from .file.schema import FileMutation
from .category.schema import CategoryQuery
from .user_following.schema import UserFollowingMutation


class Mutation(
    UserMutation,
    SampleMutation,
    FileMutation,
    UserFollowingMutation
):
    pass


class Query(
    UserQuery,
    SampleQuery,
    CategoryQuery
):
    pass
