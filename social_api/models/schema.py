from .user.schema import UserQuery, UserMutation


class Mutation(
    UserMutation
):
    pass


class Query(
    UserQuery
):
    pass
