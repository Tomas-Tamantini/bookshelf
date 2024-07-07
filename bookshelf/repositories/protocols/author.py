from typing import Protocol

from bookshelf.domain.author import Author, AuthorCore


class AuthorRepository(Protocol):
    def add(self, author: AuthorCore) -> Author: ...
