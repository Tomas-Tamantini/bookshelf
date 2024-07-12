from typing import Optional, Protocol

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import GetAuthorsDBQueryParameters, GetAuthorsDBResponse


class AuthorRepository(Protocol):
    def add(self, element: AuthorCore) -> Author: ...

    def id_exists(self, element_id: int) -> bool: ...

    def delete(self, element_id: int) -> None: ...

    def update(self, element_id: int, element: AuthorCore) -> Author: ...

    def get_by_id(self, element_id: int) -> Optional[Author]: ...

    def get_filtered(
        self, query_parameters: GetAuthorsDBQueryParameters
    ) -> GetAuthorsDBResponse: ...
