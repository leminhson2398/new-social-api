from sqlalchemy_imageattach.stores.fs import FileSystemStore
from os import path
from social_api import config, CURDIR


fs: FileSystemStore = FileSystemStore(
    path=path.join(CURDIR, 'public/images'),
    base_url=config.get('STATIC_URL_DEVELOPMENT', str)
)
