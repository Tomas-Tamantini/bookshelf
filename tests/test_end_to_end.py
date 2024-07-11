from http import HTTPStatus

import pytest


def _post_author(client, name):
    return client.post("/authors/", json={"name": name})


@pytest.mark.end_to_end
def test_author_crud(end_to_end_client):
    # Create
    response = end_to_end_client.post("/authors/", json={"name": "Clarice Lispector"})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "name": "clarice lispector"}
    # Update
    response = end_to_end_client.put("/authors/1", json={"name": "manuel bandeira"})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "manuel bandeira"}
    # Read by ID
    response = end_to_end_client.get("/authors/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "manuel bandeira"}
    # Delete
    response = end_to_end_client.delete("/authors/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Author deleted"}
    # Get by query parameters
    names = (
        "Clarice Lispector",
        "Machado de Assis",
        "Robert C.  martin",
        "Mary Shelley",
    )
    for name in names:
        _post_author(end_to_end_client, name)
    response = end_to_end_client.get("/authors?name=Ma&limit=2&offset=1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "limit": 2,
        "offset": 1,
        "total": 3,
        "authors": [
            {"id": 3, "name": "robert c martin"},
            {"id": 4, "name": "mary shelley"},
        ],
    }


@pytest.mark.end_to_end
def test_book_crud(end_to_end_client):
    # Prerequisite: Create author
    author = end_to_end_client.post("/authors/", json={"name": "Andrew Hunt"})
    author_id = author.json()["id"]
    # Create
    response = end_to_end_client.post(
        "/books/",
        json={"title": "The Pragmatic Programmer", "year": 1999, "author_id": 1},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "the pragmatic programmer",
        "year": 1999,
        "author_id": author_id,
    }
    # Update
    response = end_to_end_client.patch("/books/1", json={"year": 2000})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "title": "the pragmatic programmer",
        "year": 2000,
        "author_id": author_id,
    }
    # Read by ID
    response = end_to_end_client.get("/books/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "title": "the pragmatic programmer",
        "year": 2000,
        "author_id": author_id,
    }
    # Delete
    response = end_to_end_client.delete("/books/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Book deleted"}
    # Get by query parameters
    titles = (
        "The Pragmatic Programmer",
        "Clean Code",
        "Refactoring",
        "Clean Architecture",
    )
    for title in titles:
        end_to_end_client.post(
            "/books/",
            json={"title": title, "year": 2000, "author_id": author_id},
        )
    response = end_to_end_client.get("/books?title=Clean&limit=123&offset=1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "limit": 123,
        "offset": 1,
        "total": 2,
        "title": "clean",
        "author_id": None,
        "year": None,
        "books": [
            {
                "id": 4,
                "title": "clean architecture",
                "year": 2000,
                "author_id": author_id,
            },
        ],
    }


# TODO: Unskip
@pytest.mark.skip("Not implemented yet")
@pytest.mark.end_to_end
def test_user_crud(end_to_end_client):
    # Create
    response = end_to_end_client.post(
        "/users/",
        json={"username": " User ", "email": "a@b.com", "password": "password"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "username": "user", "email": "a@b.com"}
