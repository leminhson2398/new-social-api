from graphene import ObjectType, String, ID, Field, DateTime, Int
from .model import User


class UserType(ObjectType):
    """
        Graphql type for User model
    """
    id = Int(required=True)
    first_name = String(required=False)
    last_name = String(required=False)
    username = String(required=True)
    gender = String(required=False)
    date_of_birth = DateTime(required=False)
    email = String(required=True)
    phone_number = String(required=False)
    picture = String(required=False)


class Query(ObjectType):
    user = String(required=True)

    async def resolve_user(self, info, **kwargs):
        return "Hello"
