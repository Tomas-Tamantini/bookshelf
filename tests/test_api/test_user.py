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
