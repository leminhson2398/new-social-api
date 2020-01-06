from .import const
import typing
from starlette.datastructures import UploadFile


class CheckResult(object):
    errors: typing.List[str] = []
    validFiles: typing.List[UploadFile] = []


class FileEngine:
    def __init__(
        self,
        files: typing.List[UploadFile],
    ) -> None:
        self.files = files

    async def check_files_mimetype(self, mimetypes: typing.List[str]) -> CheckResult:
        result: CheckResult = CheckResult()
        for file in self.files:
            if file.content_type in mimetypes:
                result.validFiles.append(file)
            else:
                result.errors.append(
                    f"File {file.filename!r}: invalid mimetype: {file.content_type!r}"
                )

        return result


