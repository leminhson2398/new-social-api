from social_api.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image
from datetime import datetime


class UserPicture(Base, Image):
    __tablename__: str = 'user_pictures'
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    upload_time = Column(DateTime(), default=datetime.utcnow)
