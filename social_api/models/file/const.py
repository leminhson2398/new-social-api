import typing


DOCUMENT_TYPE: str = 'document'
PHOTO_TYPE: str = 'photo'

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
