from .import const
import typing
from starlette.datastructures import UploadFile
from social_api import ROOTDIR
from os import path
import os
from time import time


class CheckResult(object):
    errors: typing.List[str] = []


class UploadedFileProcessor:
    """
    general file processor for both image, document files
    """

    savingTemporaryPath: str = path.join(ROOTDIR, 'temp/{0}')

    def __init__(
        self,
        files: typing.List[UploadFile],
        mediaType: str
    ) -> None:
        self.files = files
        self.mediaType = mediaType
        self.checkResult = CheckResult()

    async def check_files_mimetype(self) -> 'UploadedFileProcessor':
        """
        check file mimetypes are valid or not
        Checking based on the media type provided.
        """

        validMimeTypes: typing.List[str] = const.ACCEPT_DOCUMENT_MIMETYPE if \
            self.mediaType is const.DOCUMENT_TYPE else \
            const.ACCEPT_PHOTO_MIMETYPE

        for file in self.files:
            try:
                content_type: str = getattr(file, 'content_type')
            except AttributeError:
                self.checkResult.errors.append(f"Cannot check file type.")
            else:
                if not content_type in validMimeTypes:
                    self.checkResult.errors.append(
                        f"<File {file.filename!r}: invalid mimetype: {content_type!r}>"
                    )
                    self.files.remove(file)

        return self

    async def check_file_storage_size(self) -> 'UploadedFileProcessor':
        """
        temporary save files into a directory
        get size of file by file, compare to standard size, remove invlid files
        """
        maxAllowSize: int = None
        if self.mediaType is const.DOCUMENT_TYPE:
            self.savingTemporaryPath = self.savingTemporaryPath.format(
                'documents')
            maxAllowSize = const.MAX_DOCUMENT_ALLOW_SIZE
        elif self.mediaType is const.PHOTO_TYPE:
            self.savingTemporaryPath = self.savingTemporaryPath.format(
                'images')
            maxAllowSize = const.MAX_PHOTO_ALLOW_SIZE

        # save files to a temporary folder first:
        for file in self.files:
            fileData: typing.Union[bytes, str] = await file.read()
            splitFilename: typing.List[str] = path.splitext(file.filename)
            strTimestamp: str = ''.join(str(time()).split('.'))
            newFileName: str = f"{splitFilename[0]}{strTimestamp}{splitFilename[1]}"
            fullTempFilePath: str = path.join(
                self.savingTemporaryPath, newFileName)

            # writes file to temporary folder:
            with open(fullTempFilePath, 'w' if isinstance(fileData, str) else 'wb') as tempFile:
                tempFile.write(fileData)

            # get disk file size:
            fileSize: int = path.getsize(fullTempFilePath)
            if fileSize > maxAllowSize:
                self.checkResult.errors.append(
                    f"<File {file.filename} is too big: {fileSize/1024/1024}MB>")
                # remove this invlid file:
                os.remove(fullTempFilePath)
                self.files.remove(file)

        return self
