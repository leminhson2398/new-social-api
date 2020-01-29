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
from .utils import UploadedFileProcessor, CheckResult


class FileOption(InputObjectType):
    filter = String(required=False)


class UploadFileObject(InputObjectType):
    file = Upload(required=True)
    options = FileOption(required=True)


class UploadFiles(ObjectMutation):
    ok = Boolean(required=True)
    errors = NonNull(
        List(String, required=False)
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
        if user.is_authenticated:
            files: typing.Union[typing.List[UploadFile],
                                list] = kwargs.get('files', [])
            media_type: str = kwargs.get('media_type', '').lower()

            # check files length:
            if len(files):
                fileProcessor: UploadedFileProcessor = UploadedFileProcessor(
                    files=files, mediaType=media_type)
                # check file mime types:
                check: UploadedFileProcessor = await fileProcessor.check_files_mimetype()
                check = await check.check_file_storage_size()
                print(check.checkResult.validFiles)

                for error in check.checkResult.errors:
                    errors.append(error)
            else:
                errors.append('Please choose files to upload.')
        else:
            errors.append('You have to login to upload files.')

        return UploadFiles(
            ok=ok,
            errors=errors
        )


class DeleteFiles(ObjectMutation):
    ok = Boolean(required=True)
    errors = NonNull(
        List(String, required=True)
    )

    class Argumetns:
        file_ids = NonNull(
            List()
        )


class Mutation(ObjectType):
    upload_files = UploadFiles.Field()
