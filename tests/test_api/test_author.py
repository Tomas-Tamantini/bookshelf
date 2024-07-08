from http import HTTPStatus


def test_creating_author_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/authors", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_author_returns_status_created(client):
    response = client.post("/authors", json={"name": "Andrew Hunt"})
    assert response.status_code == HTTPStatus.CREATED


def test_creating_valid_author_returns_author_with_id_given_by_repository(
    client, author_repo_mock
):
    stored_author = {"id": 123, "name": "Stored name"}

    author_repo_mock.add.return_value = stored_author

    response = client.post("/authors", json={"name": "Andrew Hunt"})
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


def test_updating_author_with_missing_fields_returns_unprocessable_entity(client):
    response = client.put("/authors/123", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_updating_existing_author_returns_status_ok(client):
    response = client.put("/authors/123", json={"name": "New name"})
    assert response.status_code == HTTPStatus.OK


def test_updating_existing_author_returns_updated_author(client, author_repo_mock):
    updated = {"id": 123, "name": "New name"}
    author_repo_mock.update.return_value = updated
    response = client.put("/authors/123", json={"name": "New name"})
    assert response.json() == updated


def test_author_name_gets_sanitized_before_being_updated(client, author_repo_mock):
    client.put("/authors/123", json={"name": "  New   Name  "})
    assert author_repo_mock.update.call_args[0][1].name == "new name"


def test_updating_author_with_nonexistent_id_returns_not_found(
    client, author_repo_mock
):
    author_repo_mock.id_exists.return_value = False
    response = client.put("/authors/123", json={"name": "New name"})
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_updating_author_with_existing_name_returns_conflict(client, author_repo_mock):
    author_repo_mock.name_exists.return_value = True

    response = client.put("/authors/123", json={"name": "existing name"})
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Author with this name already exists"}


def test_getting_author_by_id_returns_status_ok(client):
    response = client.get("/authors/123")
    assert response.status_code == HTTPStatus.OK


def test_getting_existing_author_returns_author(client, author_repo_mock):
    author = {"id": 123, "name": "Existing name"}
    author_repo_mock.get_by_id.return_value = author

    response = client.get("/authors/123")
    assert response.json() == author


def test_getting_author_with_nonexistent_id_returns_not_found(client, author_repo_mock):
    author_repo_mock.get_by_id.return_value = None
    response = client.get("/authors/123")
    assert response.status_code == HTTPStatus.NOT_FOUND
