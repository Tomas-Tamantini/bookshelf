import pytest

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import AuthorFilters, PaginationParameters
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.in_memory import InMemoryAuthorRepository
from bookshelf.repositories.relational import RelationalAuthorRepository


@pytest.fixture
def relational_repository(db_session):
    return RelationalAuthorRepository(db_session)


@pytest.fixture
def in_memory_repository():
    return InMemoryAuthorRepository()


@pytest.fixture(params=["relational_repository", "in_memory_repository"])
def repository(request):
    return request.getfixturevalue(request.param)


@pytest.mark.integration
def test_adding_author_increments_id(repository):
    auth_1 = repository.add(AuthorCore(name="Author 1"))
    assert auth_1 == Author(id=1, name="Author 1")
    auth_2 = repository.add(AuthorCore(name="Author 2"))
    assert auth_2 == Author(id=2, name="Author 2")


@pytest.mark.integration
def test_adding_author_with_existing_name_raises_conflict_error(repository):
    auth_a = AuthorCore(name="Author 1")
    repository.add(auth_a)
    auth_b = AuthorCore(name="Author 1")
    with pytest.raises(ConflictError) as exc_info:
        repository.add(auth_b)
    assert exc_info.value.field == "name"


@pytest.mark.integration
def test_author_repository_keeps_track_of_ids(repository):
    repository.add(AuthorCore(name="Author 1"))
    assert repository.id_exists(1)
    assert not repository.id_exists(2)


@pytest.mark.integration
def test_author_repository_deletes_author(repository):
    author = repository.add(AuthorCore(name="Author 1"))
    repository.delete(author.id)
    assert not repository.id_exists(author.id)


@pytest.mark.integration
def test_author_repository_updates_author(repository):
    author = repository.add(AuthorCore(name="Original"))
    updated_author = repository.update(author.id, AuthorCore(name="Updated"))
    assert updated_author == Author(id=author.id, name="Updated")


@pytest.mark.integration
def test_author_repository_raises_conflict_error_if_updating_to_existing_name(
    repository,
):
    author = repository.add(AuthorCore(name="Author 1"))
    repository.add(AuthorCore(name="Author 2"))
    with pytest.raises(ConflictError) as exc_info:
        repository.update(author.id, AuthorCore(name="Author 2"))
    assert exc_info.value.field == "name"


@pytest.mark.integration
def test_author_repository_gets_author_by_id(repository):
    author = repository.add(AuthorCore(name="Author 1"))
    assert repository.get_by_id(author.id) == author
    assert repository.get_by_id(123) is None


@pytest.mark.integration
def test_author_repository_gets_filtered_and_paginated_authors(repository):
    names = ("abc", "aab", "bba", "ccc", "cab")
    for name in names:
        repository.add(AuthorCore(name=name))
    pagination = PaginationParameters(limit=2, offset=1)
    authors_filter = AuthorFilters(name="ab")
    result = repository.get_filtered(pagination, authors_filter)
    assert result.total == 3
    assert result.elements == [Author(id=2, name="aab"), Author(id=5, name="cab")]
