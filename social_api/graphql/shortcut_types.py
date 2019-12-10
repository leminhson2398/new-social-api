from graphene import (
    Date, DateTime, ObjectType
)


class TimestampType(ObjectType):
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)
