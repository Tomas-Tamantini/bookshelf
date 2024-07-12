from http import HTTPStatus

from bookshelf.repositories.exceptions import ConflictError


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


def test_user_name_gets_sanitized_before_being_stored(
    client, mock_user_repository, valid_user_request
):
    req = valid_user_request
    req["username"] = "  User  nAmE  "
    client.post("/users", json=req)
    assert mock_user_repository.add.call_args[0][0].username == "user name"


def test_user_password_gets_hashed_before_being_stored(
    client, mock_user_repository, valid_user_request, mock_password_handler
):
    req = valid_user_request
    req["password"] = "password"
    mock_password_handler.hash.return_value = "123"
    client.post("/users", json=req)
    assert mock_password_handler.hash.call_args[0][0] == "password"
    assert mock_user_repository.add.call_args[0][0].hashed_password == "123"


def test_creating_user_with_existing_username_returns_conflict(
    client, mock_user_repository, valid_user_request
):
    mock_user_repository.add.side_effect = ConflictError("username")

    response = client.post("/users", json=valid_user_request)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "User with this username already exists"}


def test_creating_user_with_existing_email_returns_conflict(
    client, mock_user_repository, valid_user_request
):
    mock_user_repository.add.side_effect = ConflictError("email")

    response = client.post("/users", json=valid_user_request)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "User with this email already exists"}


def test_updating_user_with_missing_fields_returns_unprocessable_entity(client):
    response = client.put("/users/123", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_updating_user_with_invalid_email_returns_unprocessable_entity(
    client, valid_user_request
):
    req = valid_user_request
    req["email"] = "invalid_email"
    response = client.put("/users/123", json=req)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_updating_user_with_existing_username_returns_conflict(
    client, mock_user_repository, valid_user_request
):
    req = valid_user_request
    req["username"] = "existing"
    mock_user_repository.update.side_effect = ConflictError("username")

    response = client.put("/users/123", json=req)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "User with this username already exists"}


def test_updating_user_with_existing_email_returns_conflict(
    client, mock_user_repository, valid_user_request
):
    req = valid_user_request
    req["email"] = "existing@mail.com"
    mock_user_repository.update.side_effect = ConflictError("email")

    response = client.put("/users/123", json=req)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "User with this email already exists"}


def test_updating_user_returns_status_ok(client, valid_user_request):
    response = client.put("/users/123", json=valid_user_request)
    assert response.status_code == HTTPStatus.OK


def test_updating_user_returns_user_with_id_given_by_repository_without_password(
    client, mock_user_repository, valid_user_request
):
    stored_user = {
        "id": 123,
        "email": "a@b.com",
        "username": "user",
        "hashed_password": "password",
    }

    mock_user_repository.update.return_value = stored_user

    response = client.put("/users/123", json=valid_user_request)
    assert response.json() == {"id": 123, "email": "a@b.com", "username": "user"}


def test_user_name_gets_sanitized_before_being_updated(
    client, mock_user_repository, valid_user_request
):
    req = valid_user_request
    req["username"] = "  User  nAmE  "
    client.put("/users/123", json=req)
    assert mock_user_repository.update.call_args[0][1].username == "user name"


def test_user_password_gets_hashed_before_being_updated(
    client, mock_user_repository, valid_user_request, mock_password_handler
):
    req = valid_user_request
    req["password"] = "password"
    mock_password_handler.hash.return_value = "123"
    client.put("/users/123", json=req)
    assert mock_password_handler.hash.call_args[0][0] == "password"
    assert mock_user_repository.update.call_args[0][1].hashed_password == "123"


def test_updating_user_with_nonexistent_id_returns_not_found(
    client, mock_user_repository, valid_user_request
):
    mock_user_repository.id_exists.return_value = False
    response = client.put("/users/123", json=valid_user_request)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_getting_user_by_id_returns_status_ok(client):
    response = client.get("/users/123")
    assert response.status_code == HTTPStatus.OK


def test_getting_existing_user_returns_user_without_password(
    client, mock_user_repository
):
    user = {"id": 123, "email": "a@b.com", "username": "user", "hashed_password": "123"}
    mock_user_repository.get_by_id.return_value = user

    response = client.get("/users/123")
    assert response.json() == {"id": 123, "email": "a@b.com", "username": "user"}


def test_getting_user_with_nonexistent_id_returns_not_found(
    client, mock_user_repository
):
    mock_user_repository.get_by_id.return_value = None
    response = client.get("/users/123")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_deleting_user_returns_status_ok(client):
    response = client.delete("/users/123")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_deleting_user_delegates_to_repository(client, mock_user_repository):
    client.delete("/users/123")
    mock_user_repository.delete.assert_called_once_with(123)


def test_deleting_user_with_nonexistent_id_returns_not_found(
    client, mock_user_repository
):
    mock_user_repository.id_exists.return_value = False
    response = client.delete("/users/123")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_getting_users_returns_status_ok(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK


def test_getting_users_sanitizes_query_parameters_before_passing_to_repository(
    client, mock_user_repository
):
    client.get("/users?username=  User  &email= MaiL  ")
    assert mock_user_repository.get_filtered.call_args[0][0].username == "user"
    assert mock_user_repository.get_filtered.call_args[0][0].email == "mail"


def test_getting_users_returns_paginated_users_without_passwords(
    client, mock_user_repository, get_users_db_response
):
    mock_user_repository.get_filtered.return_value = get_users_db_response
    api_response = client.get("/users?limit=10&offset=20&username=user&email=mail")
    assert api_response.json() == {
        "limit": 10,
        "offset": 20,
        "username": "user",
        "email": "mail",
        **get_users_db_response.model_dump(),
    }
    assert mock_user_repository.get_filtered.call_args[0][0].limit == 10
    assert mock_user_repository.get_filtered.call_args[0][0].offset == 20
    assert mock_user_repository.get_filtered.call_args[0][0].username == "user"
    assert mock_user_repository.get_filtered.call_args[0][0].email == "mail"
