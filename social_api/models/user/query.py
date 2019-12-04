from graphene import ObjectType, String, ID


class Query(ObjectType):
    name = String(required=True)

    async def resolve_name(self, info, **kwargs):
        return "Hello World"
