import pytest

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.in_memory import InMemoryUserRepository


@pytest.fixture
def repository():
    return InMemoryUserRepository()


def test_adding_user_in_memory_increments_id(repository, user_core):
    req_1 = user_core(email="u1@mail.com", username="user1")
    user_1 = repository.add(req_1)
    assert user_1 == User(id=1, **req_1.model_dump())
    req_2 = user_core(email="u2@mail.com", username="user2")
    user_2 = repository.add(req_2)
    assert user_2 == User(id=2, **req_2.model_dump())


def test_adding_user_with_existing_name_in_repository_raises_conflict_error(
    repository, user_core
):
    user_a = user_core(email="u1@mail.com", username="duplicate")
    repository.add(user_a)
    user_b = user_core(email="u2@mail.com", username="duplicate")
    with pytest.raises(ConflictError) as exc_info:
        repository.add(user_b)
    assert exc_info.value.field == "username"


def test_adding_user_with_existing_email_in_repository_raises_conflict_error(
    repository, user_core
):
    user_a = user_core(email="dupli@cate.com", username="user1")
    repository.add(user_a)
    user_b = user_core(email="dupli@cate.com", username="user2")
    with pytest.raises(ConflictError) as exc_info:
        repository.add(user_b)
    assert exc_info.value.field == "email"
