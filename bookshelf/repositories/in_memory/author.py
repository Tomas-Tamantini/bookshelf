from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import (
    GetAuthorsDBQueryParameters,
    RepositoryPaginatedResponse,
)
from bookshelf.repositories.in_memory.in_memory_repository import (
    InMemoryRepository,
    RepositoryField,
)


class InMemoryAuthorRepository(InMemoryRepository[AuthorCore, Author]):
    def __init__(self) -> None:
        unique_fields = [RepositoryField("name", lambda author: author.name)]
        super().__init__(unique_fields)

    def _put_id(self, element: AuthorCore, element_id: int) -> Author:
        return Author(id=element_id, **element.model_dump())

    def _get_id(self, element: Author) -> int:
        return element.id

    def get_filtered(
        self, query_parameters: GetAuthorsDBQueryParameters
    ) -> RepositoryPaginatedResponse[Author]:
        filtered = [
            author for author in self._elements if query_parameters.name in author.name
        ]
        start_idx = query_parameters.offset
        end_idx = start_idx + query_parameters.limit
        return RepositoryPaginatedResponse[Author](
            elements=filtered[start_idx:end_idx], total=len(filtered)
        )
