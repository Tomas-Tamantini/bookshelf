from http import HTTPStatus

from fastapi.testclient import TestClient

from bookshelf.app import app


def test_health_check_returns_no_content():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == HTTPStatus.NO_CONTENT
