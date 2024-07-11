from unittest.mock import Mock

import pytest

from bookshelf.api.authentication import PasswordHandler


@pytest.fixture
def mock_password_handler():
    handler = Mock(spec=PasswordHandler)
    handler.hash.return_value = "hashed_password"
    return handler
