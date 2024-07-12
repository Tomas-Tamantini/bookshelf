from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import BookFilters
from bookshelf.repositories.in_memory.in_memory_repository import (
    InMemoryRepository,
    RepositoryField,
)


class InMemoryBookRepository(InMemoryRepository[BookCore, Book, BookFilters]):
    def __init__(self) -> None:
        unique_fields = [RepositoryField("title", lambda book: book.title)]
        super().__init__(unique_fields)

    def _put_id(self, element: BookCore, element_id: int) -> Book:
        return Book(id=element_id, **element.model_dump())

    def _get_id(self, element: Book) -> int:
        return element.id

    def _matches(self, element: Book, filters: BookFilters) -> bool:
        if filters.title is not None and filters.title not in element.title:
            return False
        if filters.author_id is not None and filters.author_id != element.author_id:
            return False
        if filters.year is not None and filters.year != element.year:
            return False
        return True
