from http import HTTPStatus


def test_creating_valid_author_returns_status_ok(client):
    response = client.post(
        "/authors",
        json={"name": "Andrew Hunt"},
    )
    assert response.status_code == HTTPStatus.OK
