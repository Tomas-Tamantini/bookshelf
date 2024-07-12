from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import AuthorFilters
from bookshelf.repositories.in_memory.in_memory_repository import (
    InMemoryRepository,
    RepositoryField,
)


class InMemoryAuthorRepository(InMemoryRepository[AuthorCore, Author, AuthorFilters]):
    def __init__(self) -> None:
        unique_fields = [RepositoryField("name", lambda author: author.name)]
        super().__init__(unique_fields)

    def _put_id(self, element: AuthorCore, element_id: int) -> Author:
        return Author(id=element_id, **element.model_dump())

    def _get_id(self, element: Author) -> int:
        return element.id

    def _matches(self, element: Author, filters: AuthorFilters) -> bool:
        return filters.name in element.name
