import pytest

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import GetUsersDBQueryParameters
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


def test_in_memory_user_repository_keeps_track_of_ids(repository, user_core):
    user = user_core()
    repository.add(user)
    assert repository.id_exists(1)
    assert not repository.id_exists(2)


def test_in_memory_user_repository_deletes_user(repository, user_core):
    user = user_core()
    user = repository.add(user)
    repository.delete(user.id)
    assert not repository.id_exists(user.id)


def test_in_memory_user_repository_updates_user(repository, user_core):
    user = user_core()
    user = repository.add(user)
    updated_user = repository.update(user.id, user_core(username="Updated"))
    assert updated_user == User(
        id=user.id, **user_core(username="Updated").model_dump()
    )


def test_in_memory_user_repository_raises_conflict_error_if_updating_to_existing_name(
    repository, user_core
):
    user = user_core(username="user1", email="a@b.com")
    user = repository.add(user)
    repository.add(user_core(username="user2", email="c@d.com"))
    with pytest.raises(ConflictError) as exc_info:
        repository.update(user.id, user_core(username="user2", email="a@b.com"))
    assert exc_info.value.field == "username"


def test_in_memory_user_repository_raises_conflict_error_if_updating_to_existing_email(
    repository, user_core
):
    user = user_core(username="user1", email="a@b.com")
    user = repository.add(user)
    repository.add(user_core(username="user2", email="c@d.com"))
    with pytest.raises(ConflictError) as exc_info:
        repository.update(user.id, user_core(username="user1", email="c@d.com"))
    assert exc_info.value.field == "email"


def test_in_memory_user_repository_gets_user_by_id(repository, user_core):
    user = user_core()
    user = repository.add(user)
    assert repository.get_by_id(user.id) == user


def test_in_memory_user_repository_gets_filtered_users(repository):
    names = ("abc", "aab", "bba", "ccc", "cab")
    for name in names:
        repository.add(
            UserCore(username=name, email=f"{name}@mail.com", hashed_password="pass")
        )
    result = repository.get_filtered(
        GetUsersDBQueryParameters(email="ab", offset=1, limit=2, username=None)
    )
    assert result.total == 3
    assert result.elements == [
        User(id=2, username="aab", email="aab@mail.com", hashed_password="pass"),
        User(id=5, username="cab", email="cab@mail.com", hashed_password="pass"),
    ]
