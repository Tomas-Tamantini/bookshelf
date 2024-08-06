import pytest

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.relational import RelationalAuthorRepository
from bookshelf.repositories.in_memory import InMemoryAuthorRepository


@pytest.fixture
def relational_repository(db_session):
    return RelationalAuthorRepository(db_session)


@pytest.fixture
def in_memory_repository():
    return InMemoryAuthorRepository()


@pytest.fixture(params=["relational_repository", "in_memory_repository"])
def repository(request):
    return request.getfixturevalue(request.param)


def test_adding_author_increments_id(repository):
    auth_1 = repository.add(AuthorCore(name="Author 1"))
    assert auth_1 == Author(id=1, name="Author 1")
    auth_2 = repository.add(AuthorCore(name="Author 2"))
    assert auth_2 == Author(id=2, name="Author 2")


def test_adding_author_with_existing_name_raises_conflict_error(repository):
    auth_a = AuthorCore(name="Author 1")
    repository.add(auth_a)
    auth_b = AuthorCore(name="Author 1")
    with pytest.raises(ConflictError) as exc_info:
        repository.add(auth_b)
    assert exc_info.value.field == "name"


def test_author_repository_keeps_track_of_ids(repository):
    repository.add(AuthorCore(name="Author 1"))
    assert repository.id_exists(1)
    assert not repository.id_exists(2)
