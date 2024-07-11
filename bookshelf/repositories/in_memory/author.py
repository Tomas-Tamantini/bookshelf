from typing import Optional

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import GetAuthorsDBQueryParameters, GetAuthorsDBResponse
from bookshelf.repositories.exceptions import ConflictError


class InMemoryAuthorRepository:
    def __init__(self):
        self._authors = []

    def add(self, author: AuthorCore) -> Author:
        if self._name_exists(author.name):
            raise ConflictError("name")
        author = Author(id=len(self._authors) + 1, **author.model_dump())
        self._authors.append(author)
        return author

    def _name_exists(self, name: str) -> bool:
        return any(author.name == name for author in self._authors)

    def id_exists(self, author_id: int) -> bool:
        return any(author.id == author_id for author in self._authors)

    def delete(self, author_id: int) -> None:
        self._authors = [author for author in self._authors if author.id != author_id]

    def update(self, author_id: int, updated: AuthorCore) -> Author:
        old_author = self.get_by_id(author_id)
        if old_author.name != updated.name and self._name_exists(updated.name):
            raise ConflictError("name")
        updated = Author(id=author_id, **updated.model_dump())
        self._authors = [
            updated if author.id == author_id else author for author in self._authors
        ]
        return updated

    def get_by_id(self, author_id: int) -> Optional[Author]:
        return next(
            (author for author in self._authors if author.id == author_id), None
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
