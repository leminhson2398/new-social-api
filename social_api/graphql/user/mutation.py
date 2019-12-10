from graphene import (
    ObjectType,
    String,
    Mutation as ObjectMutation,
    Boolean
)


class TellName(ObjectMutation):
    ok = Boolean(required=True)

    class Arguments:
        name = String(required=True)

    async def mutate(self, info, **kwargs):
        name: str = kwargs.get('name', '')
        print(name)

        return TellName(
            ok=True
        )


class Mutation(ObjectType):
    tell_name = TellName.Field()
