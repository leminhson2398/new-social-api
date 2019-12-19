from social_api.db.base import Base
from social_api.db.base import engine


# importing models for database creation:
from .user.model import User
from .file.model import UserPicture
from .sample.model import Sample
from .category.model import Category, SubCategory
from .user_following.model import UserFollowing


if not Base.metadata.is_bound():
    Base.metadata.create_all(engine)
