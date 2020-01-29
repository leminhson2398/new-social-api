import typing


DOCUMENT_TYPE: str = 'document'
PHOTO_TYPE: str = 'photo'

MAX_DOCUMENT_ALLOW_SIZE: int = 1024 * 5 * 1024
MAX_PHOTO_ALLOW_SIZE: int = 20 * 1024 * 1024

ACCEPT_DOCUMENT_MIMETYPE: typing.List[str] = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'application/pdf',
    'application/epub+zip',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
]

ACCEPT_PHOTO_MIMETYPE: typing.List[str] = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/jpg'
]
