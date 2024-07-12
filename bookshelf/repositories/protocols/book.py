from typing import Protocol

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import BookFilters

from .repository import Repository


class BookRepository(Repository[BookCore, Book, BookFilters], Protocol):
    pass
