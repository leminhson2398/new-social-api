import typing
from pydantic import BaseModel
from sqlalchemy import func
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    gender: str
    date_of_birth: datetime
    created_on: datetime
    updated_on: datetime
    active: bool

    class Config:
        orm_mode: bool = True
