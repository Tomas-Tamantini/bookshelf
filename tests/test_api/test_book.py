from http import HTTPStatus

from bookshelf.api.dto import GetBooksResponse


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


def test_updating_book_with_bad_fields_returns_unprocessable_entity(client):
    response = client.patch("/books/123", json={"bad_field": 123})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_updating_existing_book_returns_status_ok(client):
    response = client.patch("/books/123", json={"year": 2000})
    assert response.status_code == HTTPStatus.OK


def test_updating_existing_book_returns_updated_book(client, mock_book_repository):
    updated = {"id": 123, "title": "Updated title", "year": 2000, "author_id": 1}
    mock_book_repository.update.return_value = updated
    response = client.patch("/books/123", json={"year": 2000})
    assert response.json() == updated


def test_updating_book_sanitizes_new_title_before_storing(client, mock_book_repository):
    client.patch("/books/123", json={"title": "  New   Title  "})
    assert mock_book_repository.update.call_args[0][1].title == "new title"


def test_updating_book_with_nonexistent_id_returns_not_found(
    client, mock_book_repository
):
    mock_book_repository.get_by_id.return_value = None
    response = client.patch("/books/123", json={"title": "New title"})
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_updating_book_with_invalid_author_id_returns_not_found(
    client, mock_author_repository
):
    mock_author_repository.id_exists.return_value = False
    response = client.patch("/books/123", json={"author_id": 123})
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_getting_book_by_id_returns_status_ok(client):
    response = client.get("/books/123")
    assert response.status_code == HTTPStatus.OK


def test_getting_existing_book_returns_book(client, mock_book_repository):
    book = {"id": 123, "title": "Stored title", "year": 1999, "author_id": 1}
    mock_book_repository.get_by_id.return_value = book

    response = client.get("/books/123")
    assert response.json() == book


def test_getting_book_by_nonexistent_id_returns_not_found(client, mock_book_repository):
    mock_book_repository.get_by_id.return_value = None
    response = client.get("/books/123")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_getting_books_returns_status_ok(client):
    response = client.get("/books")
    assert response.status_code == HTTPStatus.OK


def test_getting_books_by_title_sanitizes_title_before_querying(
    client, mock_book_repository
):
    client.get("/books?title=  The   Pragmatic Programmer  ")
    assert (
        mock_book_repository.get_filtered.call_args[0][0].title
        == "the pragmatic programmer"
    )


def test_getting_books_returns_paginated_and_filtered_books(
    client, mock_book_repository, get_books_db_response
):
    mock_book_repository.get_filtered.return_value = get_books_db_response
    api_response = client.get("/books?title=title&offset=2&year=1999")
    assert (
        api_response.json()
        == GetBooksResponse(
            limit=20,
            offset=2,
            title="title",
            year=1999,
            author_id=None,
            **get_books_db_response.model_dump()
        ).model_dump()
    )
    assert mock_book_repository.get_filtered.call_args[0][0].title == "title"
    assert mock_book_repository.get_filtered.call_args[0][0].year == 1999
    assert mock_book_repository.get_filtered.call_args[0][0].offset == 2
