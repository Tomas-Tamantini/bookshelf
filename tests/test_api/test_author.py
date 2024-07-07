from http import HTTPStatus

from fastapi.testclient import TestClient

from bookshelf.app import app


def test_creating_valid_author_returns_status_ok():
    client = TestClient(app)
    response = client.post(
        "/authors",
        json={"name": "Andrew Hunt"},
    )
    assert response.status_code == HTTPStatus.OK
