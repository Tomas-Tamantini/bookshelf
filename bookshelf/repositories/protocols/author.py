from typing import Optional, Protocol

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import GetAuthorsDBQueryParameters, GetAuthorsDBResponse


class AuthorRepository(Protocol):
    def add(self, author: AuthorCore) -> Author: ...

    def id_exists(self, author_id: int) -> bool: ...

    def delete(self, author_id: int) -> None: ...

    def update(self, author_id: int, author: AuthorCore) -> Author: ...

    def get_by_id(self, author_id: int) -> Optional[Author]: ...

    def get_filtered(
        self, query_parameters: GetAuthorsDBQueryParameters
    ) -> GetAuthorsDBResponse: ...
