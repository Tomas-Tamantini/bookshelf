import pytest


@pytest.fixture
def valid_user_request():
    return {"email": "a@b.com", "username": "user", "password": "password"}
