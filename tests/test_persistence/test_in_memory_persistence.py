import pytest
from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.in_memory import InMemoryAuthorRepository


@pytest.fixture
def author_repo():
    return InMemoryAuthorRepository()


def test_adding_author_in_memory_increments_id(author_repo):
    auth_1 = author_repo.add(AuthorCore(name="Author 1"))
    assert auth_1 == Author(id=1, name="Author 1")
    auth_2 = author_repo.add(AuthorCore(name="Author 2"))
    assert auth_2 == Author(id=2, name="Author 2")


def test_in_memory_author_repository_keeps_track_of_existing_names(author_repo):
    author_repo.add(AuthorCore(name="Author 1"))
    assert author_repo.name_exists("Author 1")
    assert not author_repo.name_exists("Author 2")


def test_in_memory_author_repository_keeps_track_of_ids(author_repo):
    author_repo.add(AuthorCore(name="Author 1"))
    assert author_repo.id_exists(1)
    assert not author_repo.id_exists(2)


def test_in_memory_author_repository_deletes_author(author_repo):
    author = author_repo.add(AuthorCore(name="Author 1"))
    author_repo.delete(author.id)
    assert not author_repo.id_exists(author.id)


def test_in_memory_author_repository_updates_author(author_repo):
    author = author_repo.add(AuthorCore(name="Original"))
    updated_author = author_repo.update(author.id, AuthorCore(name="Updated"))
    assert updated_author == Author(id=author.id, name="Updated")
    assert author_repo.name_exists("Updated")
    assert not author_repo.name_exists("Original")


def test_in_memory_author_repository_gets_author_by_id(author_repo):
    author = author_repo.add(AuthorCore(name="Author 1"))
    assert author_repo.get_by_id(author.id) == author
    assert author_repo.get_by_id(123) is None
