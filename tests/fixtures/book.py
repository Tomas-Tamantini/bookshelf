import pytest

from bookshelf.domain.book import Book


@pytest.fixture
def book():
    return Book(id=1, title="Book Title", author_id=1, year=2021)


@pytest.fixture
def valid_book_request():
    return {"title": "The Pragmatic Programmer", "year": 1999, "author_id": 1}
