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
    stored_author = {"id": 123, "name": "Stored name"}

    author_repo_mock.add.return_value = stored_author

    response = client.post(
        "/authors",
        json={"name": "Andrew Hunt"},
    )
    assert response.json() == stored_author


def test_author_name_gets_sanitized_before_being_stored(client, author_repo_mock):
    client.post("/authors", json={"name": "  Andrew   Hunt  "})
    assert author_repo_mock.add.call_args[0][0].name == "andrew hunt"


def test_creating_author_with_existing_name_returns_conflict(client, author_repo_mock):
    author_repo_mock.name_exists.return_value = True

    response = client.post("/authors", json={"name": "Andrew Hunt"})
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Author with this name already exists"}


def test_deleting_existing_author_returns_status_ok(client):
    response = client.delete("/authors/123")
    assert response.status_code == HTTPStatus.OK


def test_deleting_existing_author_returns_success_message(client):
    response = client.delete("/authors/123")
    assert response.json() == {"message": "Author deleted"}


def test_deleting_existing_author_delegates_to_repository(client, author_repo_mock):
    client.delete("/authors/123")
    author_repo_mock.delete.assert_called_once_with(123)


def test_deleting_author_with_nonexistent_id_returns_not_found(
    client, author_repo_mock
):
    author_repo_mock.id_exists.return_value = False
    response = client.delete("/authors/123")
    assert response.status_code == HTTPStatus.NOT_FOUND
