import pytest

from bookshelf.domain.authorization import (
    DeleteUserAuthorization,
    UpdateUserAuthorization,
)
from bookshelf.domain.user import User


@pytest.fixture
def make_user():
    def _make_user(user_id: int):
        return User(id=user_id, username="n", email="a@b.com", hashed_password="p")

    return _make_user


def test_only_user_can_delete_their_own_account(make_user):
    authorization = DeleteUserAuthorization(target_id=1)
    authorized = make_user(user_id=1)
    assert authorization.has_permission(authorized)
    unauthorized = make_user(user_id=2)
    assert not authorization.has_permission(unauthorized)


def test_only_user_can_update_their_own_account(make_user):
    authorization = UpdateUserAuthorization(target_id=1)
    authorized = make_user(user_id=1)
    assert authorization.has_permission(authorized)
    unauthorized = make_user(user_id=2)
    assert not authorization.has_permission(unauthorized)
