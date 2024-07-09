from http import HTTPStatus


def test_creating_book_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/books", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_book_returns_status_created(client, valid_book_request):
    response = client.post("/books", json=valid_book_request)
    assert response.status_code == HTTPStatus.CREATED


def test_creating_valid_book_returns_book_with_id_given_by_repository(
    client, mock_book_repository, valid_book_request
):
    stored_book = {"id": 123, "title": "Stored title", "year": 1999, "author_id": 1}

    mock_book_repository.add.return_value = stored_book

    response = client.post("/books", json=valid_book_request)
    assert response.json() == stored_book


def test_book_name_gets_sanitized_beofre_being_stored(client, mock_book_repository):
    client.post(
        "/books",
        json={"title": "  The   Pragmatic Programmer  ", "year": 1999, "author_id": 1},
    )
    assert mock_book_repository.add.call_args[0][0].title == "the pragmatic programmer"


def test_creating_book_with_existing_title_returns_conflict(
    client, mock_book_repository, valid_book_request
):
    mock_book_repository.title_exists.return_value = True

    response = client.post("/books", json=valid_book_request)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Book with this title already exists"}


def test_creating_book_with_ineixsting_author_returns_not_found(
    client, mock_author_repository, valid_book_request
):
    mock_author_repository.id_exists.return_value = False

    response = client.post("/books", json=valid_book_request)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_deleting_existing_book_returns_status_ok(client):
    response = client.delete("/books/123")
    assert response.status_code == HTTPStatus.OK


def test_deleting_existing_book_returns_success_message(client):
    response = client.delete("/books/123")
    assert response.json() == {"message": "Book deleted"}


def test_deleting_existing_book_delegates_to_repository(client, mock_book_repository):
    client.delete("/books/123")
    mock_book_repository.delete.assert_called_once_with(123)


def test_deleting_book_with_nonexistent_id_returns_not_found(
    client, mock_book_repository
):
    mock_book_repository.id_exists.return_value = False
    response = client.delete("/books/123")
    assert response.status_code == HTTPStatus.NOT_FOUND
