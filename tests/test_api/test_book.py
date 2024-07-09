from http import HTTPStatus


def test_creating_book_with_missing_fields_returns_unprocessable_entity(client):
    response = client.post("/books", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_creating_valid_book_returns_status_created(client):
    response = client.post(
        "/books",
        json={"title": "The Pragmatic Programmer", "year": 1999, "author_id": 1},
    )
    assert response.status_code == HTTPStatus.CREATED


def test_creating_valid_book_returns_book_with_id_given_by_repository(
    client, mock_book_repository
):
    stored_book = {"id": 123, "title": "Stored title", "year": 1999, "author_id": 1}

    mock_book_repository.add.return_value = stored_book

    response = client.post(
        "/books",
        json={"title": "The Pragmatic Programmer", "year": 1999, "author_id": 1},
    )
    assert response.json() == stored_book


def test_book_name_gets_sanitized_beofre_being_stored(client, mock_book_repository):
    client.post(
        "/books",
        json={"title": "  The   Pragmatic Programmer  ", "year": 1999, "author_id": 1},
    )
    assert mock_book_repository.add.call_args[0][0].title == "the pragmatic programmer"
