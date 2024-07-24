from http import HTTPStatus

import pytest

from bookshelf.api.authentication import BadTokenError, Token, TokenPair
from bookshelf.api.exceptions import CredentialsError


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
    client, mock_jwt_handler, mock_user_repository, user
):
    mock_user_repository.get_by_email.return_value = user
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
    assert mock_jwt_handler.create_token_pair.call_args[0][0] == user.email


def test_refresh_token_with_bad_schema_returns_unprocessable_entity(client):
    response = client.post("auth/refresh", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_refresh_token_with_bad_token_returns_unauthorized(client, mock_jwt_handler):
    mock_jwt_handler.get_subject.side_effect = BadTokenError("bad token error msg")
    response = client.post("auth/refresh", json={"refresh_token": "bad_token"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "bad token error msg"}
    assert mock_jwt_handler.get_subject.call_args[0][0] == "bad_token"


def test_refresh_token_with_good_token_returns_new_access_token(
    client, mock_jwt_handler
):
    mock_jwt_handler.create_access_token.return_value = Token(
        access_token="new_access_token", token_type="bearer"
    )
    response = client.post("auth/refresh", json={"refresh_token": "good_token"})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "access_token": "new_access_token",
        "token_type": "bearer",
    }


def test_endpoints_that_require_authentication_return_unauthorized_if_no_token(
    dummy_auth_route_client,
):
    response = dummy_auth_route_client.get("/dummy", headers={})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_endpoints_that_require_authentication_return_unauthorized_if_bad_token(
    dummy_auth_route_client, mock_jwt_handler
):
    mock_jwt_handler.get_subject.side_effect = BadTokenError()
    response = dummy_auth_route_client.get(
        "/dummy", headers={"Authorization": "Bearer bad_token"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert mock_jwt_handler.get_subject.call_args[0][0] == "bad_token"


def test_endpoints_that_require_authentication_return_unauthorized_if_bad_email(
    dummy_auth_route_client, mock_jwt_handler, mock_user_repository
):
    mock_jwt_handler.get_subject.return_value = "bad@mail.com"
    mock_user_repository.get_by_email.return_value = None
    response = dummy_auth_route_client.get(
        "/dummy", headers={"Authorization": "Bearer good_token"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_endpoints_that_require_authentication_run_normally_if_good_token(
    dummy_auth_route_client, mock_user_repository, user
):
    mock_user_repository.get_by_email.return_value = user
    response = dummy_auth_route_client.get(
        "/dummy", headers={"Authorization": "Bearer good_token"}
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "protected_request",
    [
        lambda client: client.post("/authors", json={"name": "Andrew Hunt"}),
        lambda client: client.delete("/authors/1"),
        lambda client: client.put("/authors/1", json={"name": "Andrew Hunt"}),
        lambda client: client.post(
            "/books",
            json={"title": "The Pragmatic Programmer", "year": 1999, "author_id": 1},
        ),
        lambda client: client.delete("/books/1"),
        lambda client: client.patch("/books/1", json={"year": 2000}),
        lambda client: client.put(
            "/users/1", json={"email": "a@b.com", "username": "a", "password": "b"}
        ),
        lambda client: client.delete("/users/1"),
    ],
)
def test_endpoints_that_require_authentication_return_unauthorized_if_not_authenticated(
    protected_request, client, mock_authenticated_user_generator
):
    mock_authenticated_user_generator.get.side_effect = CredentialsError()
    response = protected_request(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
