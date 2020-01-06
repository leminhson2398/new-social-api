from .user.schema import UserQuery, UserMutation
from .file.schema import FileMutation
from .category.schema import CategoryQuery
from .user_following.schema import UserFollowingMutation


class Mutation(
    UserMutation,
    FileMutation,
    UserFollowingMutation
):
    pass


class Query(
    UserQuery,
    CategoryQuery
):
    pass
