from typing import Protocol

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import (
    BookFilters,
    PaginationParameters,
    RepositoryPaginatedResponse,
)


class BookRepository(Protocol):
    def add(self, element: BookCore) -> Book: ...

    def id_exists(self, element_id: int) -> bool: ...

    def delete(self, element_id: int) -> None: ...

    def update(self, element_id: int, book: BookCore) -> Book: ...

    def get_by_id(self, element_id: int) -> Book: ...

    def get_filtered(
        self, pagination: PaginationParameters, filters: BookFilters
    ) -> RepositoryPaginatedResponse[Book]: ...
