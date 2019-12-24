from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    ForeignKey,
    Table
)
from social_api.db.base import Base
from sqlalchemy import func
from graphene import (
    ObjectType,
    Int,
    DateTime as GDateTime
)


class UserFollowing(Base):
    __tablename__: str = 'user_following'
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(ForeignKey('users.id'))
    to_user_id = Column(ForeignKey('users.id'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


UserFollowingTable: Table = UserFollowing.__table__


class UserFollowingType(ObjectType):
    """
    graphql type for UserFollowing model
    """
    id = Int(required=False)
    from_user_id = Int(required=False)
    to_user_id = Int(required=False)
    created_at = GDateTime(required=False)
