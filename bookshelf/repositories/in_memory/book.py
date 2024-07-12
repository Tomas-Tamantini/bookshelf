from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import (
    GetBooksDBQueryParameters,
    RepositoryPaginatedResponse,
)
from bookshelf.repositories.in_memory.in_memory_repository import (
    InMemoryRepository,
    RepositoryField,
)


class InMemoryBookRepository(InMemoryRepository[BookCore, Book]):
    def __init__(self) -> None:
        unique_fields = [RepositoryField("title", lambda book: book.title)]
        super().__init__(unique_fields)

    def _put_id(self, element: BookCore, element_id: int) -> Book:
        return Book(id=element_id, **element.model_dump())

    def _get_id(self, element: Book) -> int:
        return element.id

    def get_filtered(
        self, query_parameters: GetBooksDBQueryParameters
    ) -> RepositoryPaginatedResponse[Book]:
        filtered = [
            book for book in self._elements if self._matches(book, query_parameters)
        ]
        start_idx = query_parameters.offset
        end_idx = start_idx + query_parameters.limit
        return RepositoryPaginatedResponse[Book](
            elements=filtered[start_idx:end_idx], total=len(filtered)
        )

    def _matches(self, book: Book, query_parameters: GetBooksDBQueryParameters) -> bool:
        if (
            query_parameters.title is not None
            and query_parameters.title not in book.title
        ):
            return False
        if (
            query_parameters.author_id is not None
            and query_parameters.author_id != book.author_id
        ):
            return False
        if query_parameters.year is not None and query_parameters.year != book.year:
            return False
        return True
