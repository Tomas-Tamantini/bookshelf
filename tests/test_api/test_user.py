from http import HTTPStatus


def test_creating_user_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/users", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_user_with_invalid_email_returns_unprocessable_entity(client):
    response = client.post(
        "/users",
        json={"email": "invalid_email", "username": "user", "password": "password"},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_user_returns_status_created(client):
    response = client.post(
        "/users", json={"email": "a@b.com", "username": "user", "password": "password"}
    )
    assert response.status_code == HTTPStatus.CREATED
