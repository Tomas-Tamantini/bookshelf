from typing import Optional

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import GetAuthorsDBQueryParameters, GetAuthorsDBResponse
from bookshelf.repositories.exceptions import ConflictError


class InMemoryAuthorRepository:
    def __init__(self):
        self._authors = []

    def add(self, element: AuthorCore) -> Author:
        if self._name_exists(element.name):
            raise ConflictError("name")
        author = Author(id=len(self._authors) + 1, **element.model_dump())
        self._authors.append(author)
        return author

    def _name_exists(self, name: str) -> bool:
        return any(author.name == name for author in self._authors)

    def id_exists(self, element_id: int) -> bool:
        return any(author.id == element_id for author in self._authors)

    def delete(self, element_id: int) -> None:
        self._authors = [author for author in self._authors if author.id != element_id]

    def _name_changed(self, author_id: int, author: AuthorCore) -> bool:
        old_author = self.get_by_id(author_id)
        return old_author.name != author.name

    def update(self, element_id: int, element: AuthorCore) -> Author:
        if self._name_changed(element_id, element) and self._name_exists(element.name):
            raise ConflictError("name")
        updated = Author(id=element_id, **element.model_dump())
        self._authors = [
            updated if author.id == element_id else author for author in self._authors
        ]
        return updated

    def get_by_id(self, element_id: int) -> Optional[Author]:
        return next(
            (author for author in self._authors if author.id == element_id), None
        )

    def get_filtered(
        self, query_parameters: GetAuthorsDBQueryParameters
    ) -> GetAuthorsDBResponse:
        filtered = [
            author for author in self._authors if query_parameters.name in author.name
        ]
        start_idx = query_parameters.offset
        end_idx = start_idx + query_parameters.limit
        return GetAuthorsDBResponse(
            authors=filtered[start_idx:end_idx], total=len(filtered)
        )
