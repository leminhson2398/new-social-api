from graphene import Mutation as ObjectMutation, Boolean, String, ObjectType
from starlette.background import BackgroundTasks


def printName(name: str) -> None:
    import time

    time.sleep(5)

    print(name)


class SubmitName(ObjectMutation):
    ok = Boolean(required=True)

    class Arguments:
        name = String(required=True)

    async def mutate(self, info, **kwargs):
        ok: bool = False

        name: str = kwargs.get('name', '')
        if name != '':
            ok = True

        if ok:
            background: BackgroundTasks = info.context['background']
            background.add_task(printName, name)

        return SubmitName(
            ok=ok
        )


class Mutation(ObjectType):
    submit_name = SubmitName.Field()
