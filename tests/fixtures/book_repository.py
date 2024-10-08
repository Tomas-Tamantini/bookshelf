from unittest.mock import Mock

import pytest

from bookshelf.domain.book import Book
from bookshelf.repositories.dto import RepositoryPaginatedResponse
from bookshelf.repositories.protocols import BookRepository


@pytest.fixture
def get_books_db_response():
    return RepositoryPaginatedResponse[Book](elements=[], total=100)


@pytest.fixture
def mock_book_repository(book, get_books_db_response):
    repo = Mock(spec=BookRepository)
    repo.add.return_value = book
    repo.id_exists.return_value = True
    repo.update.return_value = book
    repo.get_by_id.return_value = book
    repo.get_filtered.return_value = get_books_db_response
    return repo
