import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bookshelf.api.dependencies import (
    T_CurrentUser,
    get_author_repository,
    get_book_repository,
    get_current_user,
    get_delete_user_authorization,
    get_jwt_handler,
    get_password_handler,
    get_update_user_authorization,
    get_user_repository,
)
from bookshelf.app import app
from bookshelf.repositories.relational import (
    RelationalAuthorRepository,
    RelationalBookRepository,
    RelationalUserRepository,
)


@pytest.fixture
def client(
    mock_author_repository,
    mock_book_repository,
    mock_user_repository,
    mock_password_handler,
    mock_jwt_handler,
    mock_authenticated_user_generator,
    mock_delete_user_authorization,
    mock_update_user_authorization,
):
    with TestClient(app) as client:
        app.dependency_overrides[get_author_repository] = lambda: mock_author_repository
        app.dependency_overrides[get_book_repository] = lambda: mock_book_repository
        app.dependency_overrides[get_user_repository] = lambda: mock_user_repository
        app.dependency_overrides[get_password_handler] = lambda: mock_password_handler
        app.dependency_overrides[get_jwt_handler] = lambda: mock_jwt_handler
        app.dependency_overrides[get_current_user] = (
            lambda: mock_authenticated_user_generator.get()
        )
        app.dependency_overrides[get_delete_user_authorization] = (
            lambda: mock_delete_user_authorization
        )
        app.dependency_overrides[get_update_user_authorization] = (
            lambda: mock_update_user_authorization
        )
        yield client
        app.dependency_overrides.clear()


@pytest.fixture
def end_to_end_client(db_session):
    author_repository = RelationalAuthorRepository(db_session)
    book_repository = RelationalBookRepository(db_session)
    user_repository = RelationalUserRepository(db_session)
    with TestClient(app) as client:
        app.dependency_overrides[get_author_repository] = lambda: author_repository
        app.dependency_overrides[get_book_repository] = lambda: book_repository
        app.dependency_overrides[get_user_repository] = lambda: user_repository
        yield client
        app.dependency_overrides.clear()


@pytest.fixture
def dummy_auth_route_client(mock_jwt_handler, mock_user_repository):
    fake_app = FastAPI()

    @fake_app.get("/dummy", status_code=200)
    def dummy_route(current_user: T_CurrentUser):
        return {"dummy": "endpoint"}

    with TestClient(fake_app) as client:
        fake_app.dependency_overrides[get_jwt_handler] = lambda: mock_jwt_handler
        fake_app.dependency_overrides[get_user_repository] = (
            lambda: mock_user_repository
        )
        yield client
        fake_app.dependency_overrides.clear()
