from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean
)
from ..import Base
from datetime import datetime
from sqlalchemy_imageattach.entity import image_attachment


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=False, unique=True)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(DateTime(), nullable=True)
    email = Column(String(256), nullable=False, unique=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    # UserPicture please refer to file.mode.UserPicture
    picture = image_attachment('UserPicture')
    created_on = Column(DateTime(), default=datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    active = Column(Boolean, default=False)
