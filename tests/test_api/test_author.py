from http import HTTPStatus


def test_creating_author_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/authors", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_author_returns_status_ok(client):
    response = client.post("/authors", json={"name": "Andrew Hunt"})
    assert response.status_code == HTTPStatus.OK


def test_creating_valid_author_returns_author_with_id_given_by_repository(
    client, author_repo_mock
):
    stored_author = {
        "id": 123,
        "name": "Andrew Hunt",
    }

    author_repo_mock.add.return_value = stored_author

    response = client.post(
        "/authors",
        json={"name": "Andrew Hunt"},
    )
    assert response.json() == stored_author
