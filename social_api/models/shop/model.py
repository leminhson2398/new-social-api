from sqlalchemy import (
    Integer,
    TIMESTAMP,
    String,
    Column,
    func,
    text,
    ForeignKey,
    Boolean,
    Table,
)
from sqlalchemy.orm import relationship
from graphene import (
    Int,
    DateTime,
    String as GString
)
from social_api.db.base import Base
from social_api.utils.function import slugify
import typing


def set_name_slug(context: typing.Any) -> str:
    """
    generates slug bases on shop's name.
    """
    return slugify(
        context.get_current_parameters()['name']
    )


shopCategoryRelation: Table = Table(
    'shop_categogy_relation',
    Base.metadata,
    Column('shop_id', Integer, ForeignKey('shops.id', ondelete='CASCADE')),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE')),
    Column('enabled', Boolean, default=True),
    Column('created_at', TIMESTAMP(timezone=True), server_default=func.now())
)

shopEmployeeRelation: Table = Table(
    'shop_employee_relation',
    Base.metadata,
    Column('shop_id', Integer, ForeignKey('shops.id')),
    Column('employee_id', Integer, ForeignKey('users.id')),
    Column('role', String(20)),
    Column('enabled', Boolean, default=True),
    Column('join_since', TIMESTAMP(timezone=True), server_default=func.now())
)


class Shop(Base):
    __tablename__: str = 'shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    slug = Column(String(50), nullable=False, default=set_name_slug)
    slogan = Column(String(100))
    owner_id = Column(Integer, ForeignKey('users.id'), unique=True)
    avatar = Column(String, unique=True)
    enabled = Column(Boolean, default=False)
    phone_number = Column(String(20))
    email = Column(String(256))
    categories = relationship('Category', secondary=shopCategoryRelation)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), server_onupdate=func.now())


