import pytest

from bookshelf.domain.user import User


@pytest.fixture
def valid_user_request():
    return {"email": "a@b.com", "username": "user", "password": "password"}


@pytest.fixture
def user():
    return User(
        id=1, username="user", email="a@b.com", hashed_password="hashed_password"
    )
