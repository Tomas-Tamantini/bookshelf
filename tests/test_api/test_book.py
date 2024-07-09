from http import HTTPStatus


def test_creating_book_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/books", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
