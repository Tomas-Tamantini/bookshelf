from unittest.mock import Mock

import pytest

from bookshelf.domain.author import Author
from bookshelf.repositories.dto import RepositoryPaginatedResponse
from bookshelf.repositories.protocols import AuthorRepository


@pytest.fixture
def get_authors_db_response():
    return RepositoryPaginatedResponse[Author](elements=[], total=100)


@pytest.fixture
def mock_author_repository(author, get_authors_db_response):
    repo = Mock(spec=AuthorRepository)
    repo.add.return_value = author
    repo.get_by_id.return_value = author
    repo.update.return_value = author
    repo.id_exists.return_value = True
    repo.get_filtered.return_value = get_authors_db_response
    return repo
