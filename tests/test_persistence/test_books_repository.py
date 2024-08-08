import pytest

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import BookFilters, PaginationParameters
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.in_memory import InMemoryBookRepository
from bookshelf.repositories.relational import RelationalBookRepository


@pytest.fixture
def relational_repository(db_session):
    return RelationalBookRepository(db_session)


@pytest.fixture
def in_memory_repository():
    return InMemoryBookRepository()


@pytest.fixture(params=["relational_repository", "in_memory_repository"])
def repository(request):
    return request.getfixturevalue(request.param)


def test_adding_book_increments_id(repository):
    book_1 = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert book_1 == Book(id=1, title="Book 1", author_id=1, year=2021)
    book_2 = repository.add(BookCore(title="Book 2", author_id=2, year=2021))
    assert book_2 == Book(id=2, title="Book 2", author_id=2, year=2021)


def test_adding_book_with_existing_title_to_repository_raises_conflict_error(
    repository,
):
    repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    with pytest.raises(ConflictError):
        repository.add(BookCore(title="Book 1", author_id=2, year=2022))


def test_book_repository_keeps_track_of_ids(repository):
    repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert repository.id_exists(1)
    assert not repository.id_exists(2)


def test_book_repository_deletes_book(repository):
    book = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    repository.delete(book.id)
    assert not repository.id_exists(book.id)


def test_book_repository_updates_book(repository):
    book = repository.add(BookCore(title="Original", author_id=1, year=2021))
    updated_book = repository.update(
        book.id, BookCore(title="Updated", author_id=1, year=2021)
    )
    assert updated_book == Book(id=book.id, title="Updated", author_id=1, year=2021)


def test_updating_book_with_existing_title_repository_raises_conflict_error(
    repository,
):
    book = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    repository.add(BookCore(title="Book 2", author_id=1, year=2021))
    with pytest.raises(ConflictError):
        repository.update(book.id, BookCore(title="Book 2", author_id=1, year=2021))


def test_book_repository_gets_book_by_id(repository):
    book = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert repository.get_by_id(book.id) == book
    assert repository.get_by_id(123) is None


def test_book_repository_gets_filtered_and_paginated_books(repository):
    titles = ("abc", "aab", "bba", "ccc", "cab")
    for title in titles:
        repository.add(BookCore(title=title, author_id=1, year=2021))
    pagination = PaginationParameters(limit=2, offset=1)
    filters = BookFilters(title="ab", author_id=None, year=None)
    result = repository.get_filtered(pagination, filters)
    assert result.total == 3
    assert result.elements == [
        Book(id=2, title="aab", author_id=1, year=2021),
        Book(id=5, title="cab", author_id=1, year=2021),
    ]
