from unittest.mock import Mock

import pytest

from bookshelf.repositories.protocols import BookRepository


@pytest.fixture
def mock_book_repository(book):
    repo = Mock(spec=BookRepository)
    repo.add.return_value = book
    repo.title_exists.return_value = False
    repo.id_exists.return_value = True
    repo.update.return_value = book
    return repo
