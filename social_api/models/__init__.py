from .base import Base
from .base import engine

# importing models for database creation:
from .user.model import User
from .file.model import UserPicture
from.sample.model import Sample


if not Base.metadata.is_bound():
    Base.metadata.create_all(engine)
