from social_api.db.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    Table,
    func
)
from sqlalchemy.orm import relationship
from social_api.utils.function import slugify
import typing
from graphene import (
    Int as GInt,
    String as GString,
    ObjectType,
    DateTime as GDateTime,
    Boolean as GBoolean,
    List,
    NonNull
)
from social_api.models.shop.model import shopCategoryRelation


def set_category_slug(context: typing.Any) -> str:
    """
    return slugified version of provided string value
    """
    return slugify(
        context.get_current_parameters()['name']
    )


class CategoryGroup(Base):
    __tablename__: str = 'category_groups'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(50), nullable=False, index=True, unique=True)
    group_slug = Column(String(50), nullable=False,
                        index=True, default=set_category_slug, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=func.now(), server_onupdate=func.now())


class Category(Base):
    __tablename__: str = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True, unique=True)
    slug = Column(String(50), nullable=False, unique=True,
                  index=True, default=set_category_slug)
    group_id = Column(Integer, ForeignKey('category_groups.id'))
    enabled = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=func.now(), server_onupdate=func.now())
    shop = relationship(
        'Shop', secondary=shopCategoryRelation, back_populates='categories')


# convert to sqlalchemy core type
CategoryGroupTable: Table = CategoryGroup.__table__
CategoryTable: Table = Category.__table__


class CategoryType(ObjectType):
    """
    graphql type for Category model
    """
    id = GInt(required=False)
    name = GString(required=False)
    slug = GString(required=False)
    group_id = GString(required=False)
    enabled = GBoolean(required=False)
    created_at = GDateTime(required=False)
    updated_at = GDateTime(required=False)


class CategoryGroupType(ObjectType):
    """
    graphql type for Category model
    """
    id = GInt(required=False)
    group_name = GString(required=False)
    group_slug = GString(required=False)
    categories = NonNull(
        List(CategoryType, required=False)
    )
    created_at = GDateTime(required=False)
    updated_at = GDateTime(required=False)
