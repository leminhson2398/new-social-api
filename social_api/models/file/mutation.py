from graphene import (
    Mutation as ObjectMutation,
    Boolean,
    List,
    String,
    ObjectType,
    NonNull,
    InputObjectType
)
import typing
from starlette.authentication import BaseUser
from social_api.graphql.types import Upload
from starlette.datastructures import UploadFile
from . import const
from .utils import FileEngine, CheckResult


class FileOption(InputObjectType):
    filter = String(required=False)


class UploadFileObject(InputObjectType):
    file = Upload(required=True)
    options = FileOption(required=True)


class UploadFiles(ObjectMutation):
    ok = Boolean(required=True)
    errors = List(
        String,
        required=False
    )

    class Arguments:
        files = NonNull(
            List(UploadFileObject, required=True)
        )
        media_type = String(required=True)

    async def mutate(self, info, **kwargs):
        ok: bool = False
        errors: typing.Union[typing.List[str], list] = []

        user: BaseUser = info.context['request'].user
        # check if user is authenticated or not:
        # if user.is_authenticated:
        files: typing.Union[typing.List[UploadFile],
                            list] = kwargs.get('files', [])
        media_type: str = kwargs.get('media_type', '').lower()

        # check files length:
        if len(files):
            fileHandler: FileEngine = FileEngine(files=files)
            check: CheckResult = await fileHandler.check_files_mimetype(
                mimetypes=getattr(const, 'ACCEPT_DOCUMENT_MIMETYPE') if
                media_type == const.DOCUMENT_TYPE else 'ACCEPT_PHOTO_MIMETYPE'
            )
            if len(check.validFiles):
                print(check.validFiles)
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
