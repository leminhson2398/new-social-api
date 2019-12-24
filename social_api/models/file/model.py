from social_api.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy_imageattach.entity import Image
from sqlalchemy import func


class UserPicture(Base, Image):
    __tablename__: str = 'user_pictures'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    uploaded_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )


class ShopAvatar(Base, Image):
    __tablename__: str = 'shop_avatars'
    shop_id = Column(Integer, ForeignKey('shops.id', ondelete='CASCADE'))
    uploaded_At = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
