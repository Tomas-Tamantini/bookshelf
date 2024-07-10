import pytest
from fastapi.testclient import TestClient

from bookshelf.api.dependencies import (
    get_author_repository,
    get_book_repository,
    get_password_handler,
    get_user_repository,
)
from bookshelf.app import app
from bookshelf.repositories.in_memory import (
    InMemoryAuthorRepository,
    InMemoryBookRepository,
    InMemoryUserRepository,
)


@pytest.fixture
def client(
    mock_author_repository,
    mock_book_repository,
    mock_user_repository,
    mock_password_handler,
):
    with TestClient(app) as client:
        app.dependency_overrides[get_author_repository] = lambda: mock_author_repository
        app.dependency_overrides[get_book_repository] = lambda: mock_book_repository
        app.dependency_overrides[get_user_repository] = lambda: mock_user_repository
        app.dependency_overrides[get_password_handler] = lambda: mock_password_handler
        yield client
        app.dependency_overrides.clear()


@pytest.fixture
def end_to_end_client():
    # TODO: Use relational DB when implemented
    author_repository = InMemoryAuthorRepository()
    book_repository = InMemoryBookRepository()
    user_repository = InMemoryUserRepository()
    with TestClient(app) as client:
        app.dependency_overrides[get_author_repository] = lambda: author_repository
        app.dependency_overrides[get_book_repository] = lambda: book_repository
        app.dependency_overrides[get_user_repository] = lambda: user_repository
        yield client
        app.dependency_overrides.clear()
