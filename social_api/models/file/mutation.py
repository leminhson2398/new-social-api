from graphene import (
    Mutation as ObjectMutation,
    Boolean,
    List,
    String,
    ObjectType,
    NonNull
)
import typing
from starlette.authentication import BaseUser
from social_api.graphql.types import Upload


class UploadFiles(ObjectMutation):
    ok = Boolean(required=True)
    errors = List(
        String,
        required=False
    )

    class Arguments:
        files = NonNull(
            List(Upload, required=True)
        )

    async def mutate(self, info, **kwargs):
        ok: bool = False
        errors: typing.Union[typing.List[str], list] = []

        user: BaseUser = info.context['request'].user
        # check user is authenticated or not:
        # if user.is_authenticated:
        files: typing.List[typing.Any] = kwargs.get('files', [])
        # check files list length:
        if len(files):
            ok = True
            print(files)
        else:
            errors.append('Please choose files to upload.')
        # else:
        #     errors.append('You have to login to upload files.')

        return UploadFiles(
            ok=ok,
            errors=errors
        )


class Mutation(ObjectType):
    upload_files = UploadFiles.Field()
