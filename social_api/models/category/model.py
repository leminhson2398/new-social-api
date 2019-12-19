from social_api.db.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Table
)
from datetime import datetime
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


def set_category_slug(context: typing.Any) -> str:
    """
    return slugified version of provided string value
    """
    return slugify(
        context.get_current_parameters()['name']
    )


class Category(Base):
    __tablename__: str = 'categories'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True, unique=True)
    slug = Column(String(50), nullable=False,
                  index=True, default=set_category_slug, unique=True)
    enabled = Column(Boolean(), default=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(), nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)


class SubCategory(Base):
    __tablename__: str = 'sub_categories'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    slug = Column(String(50), nullable=False,
                  index=True, default=set_category_slug)
    parent_id = Column(ForeignKey('categories.id'))
    enabled = Column(Boolean(), default=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(), nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)


# convert to sqlalchemy core type
CategoryTable: Table = Category.__table__
SubCategoryTable: Table = SubCategory.__table__


class SubCategoryType(ObjectType):
    """
    graphql type for Category model
    """
    id = GInt(required=False)
    name = GString(required=False)
    slug = GString(required=False)
    parent_id = GString(required=False)
    enabled = GBoolean(required=False)
    created_at = GDateTime(required=False)
    updated_at = GDateTime(required=False)


class CategoryType(ObjectType):
    """
    graphql type for Category model
    """
    id = GInt(required=False)
    name = GString(required=False)
    slug = GString(required=False)
    enabled = GBoolean(required=False)
    sub_categories = NonNull(
        List(SubCategoryType, required=False)
    )
    created_at = GDateTime(required=False)
    updated_at = GDateTime(required=False)
