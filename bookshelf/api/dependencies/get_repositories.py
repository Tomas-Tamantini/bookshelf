from typing import Annotated

from fastapi import Depends

from bookshelf.repositories.in_memory import InMemoryAuthorRepository
from bookshelf.repositories.protocols import AuthorRepository

in_memory_repo = InMemoryAuthorRepository()


def get_author_repository() -> AuthorRepository:
    return in_memory_repo


T_AuthorRepository = Annotated[AuthorRepository, Depends(get_author_repository)]
