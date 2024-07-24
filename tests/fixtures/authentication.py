from typing import Protocol
from unittest.mock import Mock

import pytest

from bookshelf.api.authentication import JWTHandler, PasswordHandler, TokenPair
from bookshelf.domain.user import User


@pytest.fixture
def mock_password_handler():
    handler = Mock(spec=PasswordHandler)
    handler.hash.return_value = "hashed_password"
    return handler


@pytest.fixture
def mock_jwt_handler():
    handler = Mock(spec=JWTHandler)
    handler.create_token_pair.return_value = TokenPair(
        access_token="access_token", refresh_token="refresh_token", token_type="bearer"
    )
    handler.get_subject.return_value = "test_subject"
    return handler


class _AuthenticatedUserGenerator(Protocol):
    def get(self) -> User: ...


@pytest.fixture
def mock_authenticated_user_generator(user):
    generator = Mock(spec=_AuthenticatedUserGenerator)
    generator.get.return_value = user
    return generator
