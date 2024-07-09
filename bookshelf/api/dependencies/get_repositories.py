from typing import Annotated

from fastapi import Depends

from bookshelf.repositories.in_memory import (
    InMemoryAuthorRepository,
    InMemoryBookRepository,
)
from bookshelf.repositories.protocols import AuthorRepository, BookRepository

in_memory_repo = InMemoryAuthorRepository()
in_memory_book_repo = InMemoryBookRepository()


def get_author_repository() -> AuthorRepository:
    return in_memory_repo


def get_book_repository() -> BookRepository:
    return in_memory_book_repo


T_AuthorRepository = Annotated[AuthorRepository, Depends(get_author_repository)]
T_BookRepository = Annotated[BookRepository, Depends(get_book_repository)]
