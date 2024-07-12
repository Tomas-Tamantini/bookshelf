import pytest

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import GetBooksDBQueryParameters
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.in_memory import InMemoryBookRepository


@pytest.fixture
def repository():
    return InMemoryBookRepository()


def test_adding_book_in_memory_increments_id(repository):
    book_1 = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert book_1 == Book(id=1, title="Book 1", author_id=1, year=2021)
    book_2 = repository.add(BookCore(title="Book 2", author_id=2, year=2021))
    assert book_2 == Book(id=2, title="Book 2", author_id=2, year=2021)


def test_adding_book_with_existing_title_to_in_memory_repository_raises_conflict_error(
    repository,
):
    repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    with pytest.raises(ConflictError):
        repository.add(BookCore(title="Book 1", author_id=2, year=2022))


def test_in_memory_book_repository_keeps_track_of_ids(repository):
    repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert repository.id_exists(1)
    assert not repository.id_exists(2)


def test_in_memory_book_repository_deletes_book(repository):
    book = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    repository.delete(book.id)
    assert not repository.id_exists(book.id)


def test_in_memory_book_repository_updates_book(repository):
    book = repository.add(BookCore(title="Original", author_id=1, year=2021))
    updated_book = repository.update(
        book.id, BookCore(title="Updated", author_id=1, year=2021)
    )
    assert updated_book == Book(id=book.id, title="Updated", author_id=1, year=2021)


def test_updating_book_with_existing_title_in_memory_repository_raises_conflict_error(
    repository,
):
    book = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    repository.add(BookCore(title="Book 2", author_id=1, year=2021))
    with pytest.raises(ConflictError):
        repository.update(book.id, BookCore(title="Book 2", author_id=1, year=2021))


def test_in_memory_book_repository_gets_book_by_id(repository):
    book = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert repository.get_by_id(book.id) == book
    assert repository.get_by_id(123) is None


def test_in_memory_book_repository_gets_filtered_and_paginated_books(repository):
    titles = ("abc", "aab", "bba", "ccc", "cab")
    for title in titles:
        repository.add(BookCore(title=title, author_id=1, year=2021))
    result = repository.get_filtered(
        GetBooksDBQueryParameters(
            title="ab", limit=2, offset=1, author_id=None, year=None
        )
    )
    assert result.total == 3
    assert result.elements == [
        Book(id=2, title="aab", author_id=1, year=2021),
        Book(id=5, title="cab", author_id=1, year=2021),
    ]
