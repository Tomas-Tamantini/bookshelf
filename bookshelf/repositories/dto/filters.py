from typing import Optional

from pydantic import BaseModel


class AuthorFilters(BaseModel):
    name: str


class BookFilters(BaseModel):
    title: Optional[str]
    author_id: Optional[int]
    year: Optional[int]


class UserFilters(BaseModel):
    username: Optional[str]
    email: Optional[str]
