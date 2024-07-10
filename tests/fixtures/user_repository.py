from unittest.mock import Mock

import pytest

from bookshelf.repositories.protocols import UserRepository


@pytest.fixture
def mock_user_repository(user):
    repo = Mock(spec=UserRepository)
    repo.add.return_value = user
    return repo
