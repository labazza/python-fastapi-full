# import this so you dont have to map column order to field order
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from sqlalchemy.sql.sqltypes import Boolean, Enum

from .database import Base


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    # allow pydantic to work with orm too
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    # pydantic will convert number to sring
    # if title is for example 1 from post request
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # allow pydantic to work with orm too
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    # it is called Post capitalized from the object expected
    Post: Post
    votes: int


class PostCreate(PostBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Votes(BaseModel):
    post_id: int
    dir: conint(le=1)
