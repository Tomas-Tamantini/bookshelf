from typing import Protocol

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import GetBooksDBQueryParameters, GetBooksDBResponse


class BookRepository(Protocol):
    def add(self, book: BookCore) -> Book: ...

    def id_exists(self, book_id: int) -> bool: ...

    def delete(self, book_id: int) -> None: ...

    def update(self, book_id: int, book: BookCore) -> Book: ...

    def get_by_id(self, book_id: int) -> Book: ...

    def get_filtered(
        self, query_parameters: GetBooksDBQueryParameters
    ) -> GetBooksDBResponse: ...
