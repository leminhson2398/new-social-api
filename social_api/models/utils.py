from graphene import DateTime, ObjectType


class CreateUpdateTimeBaseType(ObjectType):
    """
    use it if your sqlalchemy model has two timestamp fields:
    created_at, updated_at
    """
    created_at = DateTime(required=True)
    updated_at = DateTime(required=True)


class CreateTimeBaseType(ObjectType):
    """
    use it if your sqlalchemy model has only 1 timestamp field: created_at
    """
    created_at = DateTime(required=True)
