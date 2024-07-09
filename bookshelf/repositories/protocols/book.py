from typing import Protocol

from bookshelf.domain.book import Book, BookCore


class BookRepository(Protocol):
    def add(self, book: BookCore) -> Book: ...

    def title_exists(self, title: str) -> bool: ...
