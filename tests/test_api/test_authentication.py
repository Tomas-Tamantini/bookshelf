from http import HTTPStatus

from bookshelf.api.authentication import TokenPair


def test_login_with_bad_schema_returns_unprocessable_entity(client):
    response = client.post("auth/login", data={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_login_with_bad_email_returns_unauthorized(client, mock_user_repository):
    mock_user_repository.get_by_email.return_value = None
    response = client.post(
        "auth/login", data={"username": "bad@mail.com", "password": "123"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}
    assert mock_user_repository.get_by_email.call_args[0][0] == "bad@mail.com"


def test_login_with_bad_password_returns_unauthorized(client, mock_password_handler):
    mock_password_handler.verify.return_value = False
    response = client.post(
        "auth/login", data={"username": "good@email.com", "password": "bad_password"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


def test_login_with_good_credentials_returns_jwt_access_and_refresh_tokens(
    client, mock_jwt_handler
):
    mock_jwt_handler.create_token_pair.return_value = TokenPair(
        access_token="access_token", refresh_token="refresh_token", token_type="bearer"
    )

    response = client.post(
        "auth/login", data={"username": "good@email.com", "password": "good_password"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
        "token_type": "bearer",
    }
