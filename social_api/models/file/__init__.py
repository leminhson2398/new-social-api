from sqlalchemy_imageattach.stores.fs import FileSystemStore
from os import path
from social_api import config, ROOTDIR


fs: FileSystemStore = FileSystemStore(
    path=path.join(ROOTDIR, 'public/images'),
    base_url=config.get('STATIC_URL_DEVELOPMENT', str)
)
