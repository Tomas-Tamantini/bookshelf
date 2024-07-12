from unittest.mock import Mock

import pytest

from bookshelf.domain.user import User
from bookshelf.repositories.dto import RepositoryPaginatedResponse
from bookshelf.repositories.protocols import UserRepository


@pytest.fixture
def get_users_db_response():
    return RepositoryPaginatedResponse[User](elements=[], total=100)


@pytest.fixture
def mock_user_repository(user, get_users_db_response):
    repo = Mock(spec=UserRepository)
    repo.add.return_value = user
    repo.update.return_value = user
    repo.id_exists.return_value = True
    repo.get_by_id.return_value = user
    repo.get_filtered.return_value = get_users_db_response
    return repo
