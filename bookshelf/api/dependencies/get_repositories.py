from typing import Annotated

from fastapi import Depends

from bookshelf.repositories.relational import (
    RelationalAuthorRepository,
    RelationalBookRepository,
    RelationalUserRepository,
)
from bookshelf.repositories.protocols import (
    AuthorRepository,
    BookRepository,
    UserRepository,
)
from bookshelf.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


db_url = Settings().DATABASE_URL
engine = create_engine(db_url)
session = Session(engine)


def get_author_repository() -> AuthorRepository:
    return RelationalAuthorRepository(session)


def get_book_repository() -> BookRepository:
    return RelationalBookRepository(session)


def get_user_repository() -> UserRepository:
    return RelationalUserRepository(session)


T_AuthorRepository = Annotated[AuthorRepository, Depends(get_author_repository)]
T_BookRepository = Annotated[BookRepository, Depends(get_book_repository)]
T_UserRepository = Annotated[UserRepository, Depends(get_user_repository)]
