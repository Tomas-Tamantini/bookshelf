from http import HTTPStatus


def test_creating_user_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/users", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
