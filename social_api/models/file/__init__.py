from sqlalchemy_imageattach.stores.fs import FileSystemStore
from ..import CURDIR
from os import path
from ...import config


fs: FileSystemStore = FileSystemStore(
    path=path.join(CURDIR, 'public/images'),
    base_url=config.get('STATIC_URL_DEVELOPMENT', '')
)
