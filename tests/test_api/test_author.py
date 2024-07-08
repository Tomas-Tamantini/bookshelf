from http import HTTPStatus


def test_creating_author_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/authors", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_author_returns_status_created(client):
    response = client.post("/authors", json={"name": "Andrew Hunt"})
    assert response.status_code == HTTPStatus.CREATED


def test_creating_valid_author_returns_author_with_id_given_by_repository(
    client, mock_author_repository
):
    stored_author = {"id": 123, "name": "Stored name"}

    mock_author_repository.add.return_value = stored_author

    response = client.post("/authors", json={"name": "Andrew Hunt"})
    assert response.json() == stored_author


def test_author_name_gets_sanitized_before_being_stored(client, mock_author_repository):
    client.post("/authors", json={"name": "  Andrew   Hunt  "})
    assert mock_author_repository.add.call_args[0][0].name == "andrew hunt"


def test_creating_author_with_existing_name_returns_conflict(
    client, mock_author_repository
):
    mock_author_repository.name_exists.return_value = True

    response = client.post("/authors", json={"name": "Andrew Hunt"})
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Author with this name already exists"}


def test_deleting_existing_author_returns_status_ok(client):
    response = client.delete("/authors/123")
    assert response.status_code == HTTPStatus.OK


def test_deleting_existing_author_returns_success_message(client):
    response = client.delete("/authors/123")
    assert response.json() == {"message": "Author deleted"}


def test_deleting_existing_author_delegates_to_repository(
    client, mock_author_repository
):
    client.delete("/authors/123")
    mock_author_repository.delete.assert_called_once_with(123)


def test_deleting_author_with_nonexistent_id_returns_not_found(
    client, mock_author_repository
):
    mock_author_repository.id_exists.return_value = False
    response = client.delete("/authors/123")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_updating_author_with_missing_fields_returns_unprocessable_entity(client):
    response = client.put("/authors/123", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_updating_existing_author_returns_status_ok(client):
    response = client.put("/authors/123", json={"name": "New name"})
    assert response.status_code == HTTPStatus.OK


def test_updating_existing_author_returns_updated_author(
    client, mock_author_repository
):
    updated = {"id": 123, "name": "New name"}
    mock_author_repository.update.return_value = updated
    response = client.put("/authors/123", json={"name": "New name"})
    assert response.json() == updated


def test_author_name_gets_sanitized_before_being_updated(
    client, mock_author_repository
):
    client.put("/authors/123", json={"name": "  New   Name  "})
    assert mock_author_repository.update.call_args[0][1].name == "new name"


def test_updating_author_with_nonexistent_id_returns_not_found(
    client, mock_author_repository
):
    mock_author_repository.id_exists.return_value = False
    response = client.put("/authors/123", json={"name": "New name"})
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_updating_author_with_existing_name_returns_conflict(
    client, mock_author_repository
):
    mock_author_repository.name_exists.return_value = True

    response = client.put("/authors/123", json={"name": "existing name"})
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Author with this name already exists"}


def test_getting_author_by_id_returns_status_ok(client):
    response = client.get("/authors/123")
    assert response.status_code == HTTPStatus.OK


def test_getting_existing_author_returns_author(client, mock_author_repository):
    author = {"id": 123, "name": "Existing name"}
    mock_author_repository.get_by_id.return_value = author

    response = client.get("/authors/123")
    assert response.json() == author


def test_getting_author_with_nonexistent_id_returns_not_found(
    client, mock_author_repository
):
    mock_author_repository.get_by_id.return_value = None
    response = client.get("/authors/123")
    assert response.status_code == HTTPStatus.NOT_FOUND
