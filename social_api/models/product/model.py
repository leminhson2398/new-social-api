from ..import Base
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean
)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
