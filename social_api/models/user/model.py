from sqlalchemy import (
    Column, String, Integer, TIMESTAMP, Boolean, Table, func, text
)
from graphene import (
    ObjectType,
    String as GString,
    Int,
    Boolean as GBoolean,
    Date,
    DateTime as GDateTime
)
from sqlalchemy_imageattach.entity import image_attachment
from social_api.db.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__: str = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=False, unique=True)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(TIMESTAMP(timezone=True), nullable=True)
    email = Column(String(256), nullable=True, unique=True, index=True)
    phone_number = Column(String(15), nullable=True, unique=True)
    hashed_password = Column(String(200), nullable=False)
    # UserPicture please refer to file.mode.UserPicture
    picture = image_attachment('UserPicture')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False,
                        onupdate=func.now())
    active = Column(Boolean, default=False)
    number_of_followers = Column(Integer, default=text('0'))
    shop = relationship('Shop', uselist=False, back_populates='owner')


class UserType(ObjectType):
    """
        Graphql type for User model
    """
    id = Int(required=False)
    first_name = GString(required=False)
    last_name = GString(required=False)
    username = GString(required=False)
    gender = GString(required=False)
    date_of_birth = Date(required=False)
    email = GString(required=False)
    phone_number = GString(required=False)
    picture = GString(required=False)
    active = GBoolean(required=False)
    created_at = GDateTime(required=False)
    updated_at = GDateTime(required=False)
    number_of_followers = Int(required=False)


UserTable: Table = User.__table__
