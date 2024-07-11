import pytest

from bookshelf.domain.user import User, UserCore


@pytest.fixture
def valid_user_request():
    return {"email": "a@b.com", "username": "user", "password": "password"}


@pytest.fixture
def user():
    return User(
        id=1, username="user", email="a@b.com", hashed_password="hashed_password"
    )


@pytest.fixture
def user_core():
    def _build_user(
        email: str = "user@email.com",
        username: str = "user",
        hashed_password: str = "hashed_password",
    ):
        return UserCore(email=email, username=username, hashed_password=hashed_password)

    return _build_user
