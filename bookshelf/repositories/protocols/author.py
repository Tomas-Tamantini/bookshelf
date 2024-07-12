from typing import Protocol

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import AuthorFilters

from .repository import Repository


class AuthorRepository(Repository[AuthorCore, Author, AuthorFilters], Protocol):
    pass
