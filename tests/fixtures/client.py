import pytest
from fastapi.testclient import TestClient

from bookshelf.api.dependencies import get_author_repository
from bookshelf.app import app


@pytest.fixture
def client(author_repo_mock):
    with TestClient(app) as client:
        app.dependency_overrides[get_author_repository] = lambda: author_repo_mock
        yield client
        app.dependency_overrides.clear()
