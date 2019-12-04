from ..import Base
from ...import CURDIR
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from ..user.model import User
from sqlalchemy_imageattach.entity import Image


class UserPicture(Base, Image):
    __tablename__: str = 'user_pictures'
    user_id = Column(Integer, ForeignKey('user.id', primary_key=True))
    user = relationship('User')
