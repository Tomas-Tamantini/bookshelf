from dataclasses import dataclass

import pytest

from bookshelf.domain.author import AuthorCore
from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import BookFilters, PaginationParameters
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.in_memory import InMemoryBookRepository
from bookshelf.repositories.protocols import BookRepository
from bookshelf.repositories.relational import (
    RelationalAuthorRepository,
    RelationalBookRepository,
)


@dataclass(frozen=True)
class _BookRepoWithValidAuthorId:
    repository: BookRepository
    author_id: int


@pytest.fixture
def relational(db_session):
    author_repo = RelationalAuthorRepository(db_session)
    author = AuthorCore(name="Andrew Hunt")
    author_with_id = author_repo.add(author)
    book_repo = RelationalBookRepository(db_session)
    return _BookRepoWithValidAuthorId(repository=book_repo, author_id=author_with_id.id)


@pytest.fixture
def in_memory():
    return _BookRepoWithValidAuthorId(repository=InMemoryBookRepository(), author_id=1)


@pytest.fixture(params=["relational", "in_memory"])
def repository_with_author_id(request):
    return request.getfixturevalue(request.param)

@pytest.mark.integration
def test_adding_book_increments_id(repository_with_author_id):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    book_1 = repository.add(BookCore(title="Book 1", author_id=author_id, year=2021))
    assert book_1 == Book(id=1, title="Book 1", author_id=author_id, year=2021)
    book_2 = repository.add(BookCore(title="Book 2", author_id=author_id, year=2021))
    assert book_2 == Book(id=2, title="Book 2", author_id=author_id, year=2021)

@pytest.mark.integration
def test_adding_book_with_existing_title_to_repository_raises_conflict_error(
    repository_with_author_id,
):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    repository.add(BookCore(title="Book 1", author_id=author_id, year=2021))
    with pytest.raises(ConflictError):
        repository.add(BookCore(title="Book 1", author_id=author_id, year=2022))

@pytest.mark.integration
def test_book_repository_keeps_track_of_ids(repository_with_author_id):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    repository.add(BookCore(title="Book 1", author_id=author_id, year=2021))
    assert repository.id_exists(1)
    assert not repository.id_exists(2)

@pytest.mark.integration
def test_book_repository_deletes_book(repository_with_author_id):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    book = repository.add(BookCore(title="Book 1", author_id=author_id, year=2021))
    repository.delete(book.id)
    assert not repository.id_exists(book.id)

@pytest.mark.integration
def test_book_repository_updates_book(repository_with_author_id):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    book = repository.add(BookCore(title="Original", author_id=author_id, year=2021))
    updated_book = repository.update(
        book.id, BookCore(title="Updated", author_id=author_id, year=2021)
    )
    assert updated_book == Book(
        id=book.id, title="Updated", author_id=author_id, year=2021
    )

@pytest.mark.integration
def test_updating_book_with_existing_title_repository_raises_conflict_error(
    repository_with_author_id,
):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    book = repository.add(BookCore(title="Book 1", author_id=author_id, year=2021))
    repository.add(BookCore(title="Book 2", author_id=author_id, year=2021))
    with pytest.raises(ConflictError):
        repository.update(
            book.id, BookCore(title="Book 2", author_id=author_id, year=2021)
        )

@pytest.mark.integration
def test_book_repository_gets_book_by_id(repository_with_author_id):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    book = repository.add(BookCore(title="Book 1", author_id=author_id, year=2021))
    assert repository.get_by_id(book.id) == book
    assert repository.get_by_id(123) is None

@pytest.mark.integration
def test_book_repository_gets_filtered_and_paginated_books(repository_with_author_id):
    repository = repository_with_author_id.repository
    author_id = repository_with_author_id.author_id
    titles = ("abc", "aab", "bba", "ccc", "cab")
    for title in titles:
        repository.add(BookCore(title=title, author_id=author_id, year=2021))
    pagination = PaginationParameters(limit=2, offset=1)
    filters = BookFilters(title="ab", author_id=None, year=None)
    result = repository.get_filtered(pagination, filters)
    assert result.total == 3
    assert result.elements == [
        Book(id=2, title="aab", author_id=author_id, year=2021),
        Book(id=5, title="cab", author_id=author_id, year=2021),
    ]
