import pytest

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import GetAuthorsDBQueryParameters
from bookshelf.repositories.in_memory import InMemoryAuthorRepository


@pytest.fixture
def repository():
    return InMemoryAuthorRepository()


def test_adding_author_in_memory_increments_id(repository):
    auth_1 = repository.add(AuthorCore(name="Author 1"))
    assert auth_1 == Author(id=1, name="Author 1")
    auth_2 = repository.add(AuthorCore(name="Author 2"))
    assert auth_2 == Author(id=2, name="Author 2")


def test_in_memory_author_repository_keeps_track_of_existing_names(repository):
    repository.add(AuthorCore(name="Author 1"))
    assert repository.name_exists("Author 1")
    assert not repository.name_exists("Author 2")


def test_in_memory_author_repository_keeps_track_of_ids(repository):
    repository.add(AuthorCore(name="Author 1"))
    assert repository.id_exists(1)
    assert not repository.id_exists(2)


def test_in_memory_author_repository_deletes_author(repository):
    author = repository.add(AuthorCore(name="Author 1"))
    repository.delete(author.id)
    assert not repository.id_exists(author.id)


def test_in_memory_author_repository_updates_author(repository):
    author = repository.add(AuthorCore(name="Original"))
    updated_author = repository.update(author.id, AuthorCore(name="Updated"))
    assert updated_author == Author(id=author.id, name="Updated")
    assert repository.name_exists("Updated")
    assert not repository.name_exists("Original")


def test_in_memory_author_repository_gets_author_by_id(repository):
    author = repository.add(AuthorCore(name="Author 1"))
    assert repository.get_by_id(author.id) == author
    assert repository.get_by_id(123) is None


def test_in_memory_author_repository_gets_filtered_and_paginated_authors(repository):
    names = ("abc", "aab", "bba", "ccc", "cab")
    for name in names:
        repository.add(AuthorCore(name=name))
    resullt = repository.get_filtered(
        GetAuthorsDBQueryParameters(name="ab", limit=2, offset=1)
    )
    assert resullt.total == 3
    assert resullt.authors == [Author(id=2, name="aab"), Author(id=5, name="cab")]