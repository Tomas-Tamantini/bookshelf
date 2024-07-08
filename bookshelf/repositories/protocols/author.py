from typing import Protocol

from bookshelf.domain.author import Author, AuthorCore


class AuthorRepository(Protocol):
    def add(self, author: AuthorCore) -> Author: ...

    def name_exists(self, name: str) -> bool: ...
