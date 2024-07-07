from http import HTTPStatus


def test_creating_author_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/authors", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_author_returns_status_ok(client):
    response = client.post("/authors", json={"name": "Andrew Hunt"})
    assert response.status_code == HTTPStatus.OK


def test_creating_valid_author_returns_author_with_id(client):
    response = client.post(
        "/authors",
        json={"name": "Andrew Hunt"},
    )
    assert response.json()["id"] == 1
