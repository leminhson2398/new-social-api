from graphene import (
    Mutation as ObjectMutation,
    String,
    Int,
    Boolean,
    List,
    NonNull
)


class AddCategory(ObjectMutation):
    ok = Boolean(required=True)
    errors = NonNull(
        List(String, required=False)
    )

    class Arguments:
        name = String(required=True)

    async def mutate(self, info, **kwargs):
        pass
