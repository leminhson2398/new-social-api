from .base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .user import User
from sqlalchemy_imageattach.entity import Image


class UserPicture(Base, Image):
    __tablename__: str = 'user_pictures'
    user_id = Column(Integer, ForeignKey('users.id', primary_key=True))
    user = relationship('User')
