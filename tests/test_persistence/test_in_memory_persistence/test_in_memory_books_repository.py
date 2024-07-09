import pytest

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.in_memory import InMemoryBookRepository


@pytest.fixture
def repository():
    return InMemoryBookRepository()


def test_adding_book_in_memory_increments_id(repository):
    book_1 = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert book_1 == Book(id=1, title="Book 1", author_id=1, year=2021)
    book_2 = repository.add(BookCore(title="Book 2", author_id=2, year=2021))
    assert book_2 == Book(id=2, title="Book 2", author_id=2, year=2021)


def test_in_memory_book_repository_keeps_track_of_existing_titles(repository):
    repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert repository.title_exists("Book 1")
    assert not repository.title_exists("Book 2")


def test_in_memory_book_repository_keeps_track_of_ids(repository):
    repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    assert repository.id_exists(1)
    assert not repository.id_exists(2)


def test_in_memory_book_repository_deletes_book(repository):
    book = repository.add(BookCore(title="Book 1", author_id=1, year=2021))
    repository.delete(book.id)
    assert not repository.id_exists(book.id)
