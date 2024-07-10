from http import HTTPStatus


def test_creating_user_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/users", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_user_with_invalid_email_returns_unprocessable_entity(
    client, valid_user_request
):
    req = valid_user_request
    req["email"] = "invalid_email"
    response = client.post("/users", json=req)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_user_returns_status_created(client, valid_user_request):
    response = client.post("/users", json=valid_user_request)
    assert response.status_code == HTTPStatus.CREATED


def test_creating_valid_user_returns_user_with_id_given_by_repository_without_password(
    client, mock_user_repository, valid_user_request
):
    stored_user = {
        "id": 123,
        "email": "a@b.com",
        "username": "user",
        "hashed_password": "password",
    }

    mock_user_repository.add.return_value = stored_user

    response = client.post("/users", json=valid_user_request)
    assert response.json() == {"id": 123, "email": "a@b.com", "username": "user"}


def test_user_name_gets_sanitized_before_being_stored(client, mock_user_repository):
    client.post(
        "/users",
        json={"email": "a@b.com", "username": "  User  nAmE  ", "password": "password"},
    )
    assert mock_user_repository.add.call_args[0][0].username == "user name"
