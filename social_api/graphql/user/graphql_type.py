from graphene import (
    Int,
    String,
    Date,
    DateTime,
    Boolean,
    ObjectType
)


class UserType(ObjectType):
    id = Int(required=True)
    first_name = String(required=False)
    last_name = String(required=False)
    username = String(required=True)
    # gender will be set to 'other' if user not provide it
    gender = String(required=True)
    date_of_birth = Date(required=False)
    email = String(required=True)
    phone_number = String(required=False)
    # picture not implemented properly:
    picture = String(required=False)
    created_on = DateTime(required=True)
    updated_on = DateTime(required=True)
    active = Boolean(required=True)
