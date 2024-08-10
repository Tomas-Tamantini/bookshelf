from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from freezegun import freeze_time

from bookshelf.settings import Settings

# TODO: Refactor tests - Lots of duplication


def _post_author(client, name, token):
    return client.post(
        "/authors/",
        json={"name": name},
        headers={"Authorization": f"Bearer {token}"},
    )


# TODO: Remove all the duplicate headers
# TODO: Extract prerequisites into fixtures
@pytest.mark.end_to_end
def test_author_crud(end_to_end_client):
    # Prerequisite: Create user and login
    # Create user
    end_to_end_client.post(
        "/users/",
        json={"username": "user", "email": "a@b.com", "password": "123"},
    )
    # Login
    response = end_to_end_client.post(
        "/auth/login", data={"username": "a@b.com", "password": "123"}
    )
    token = response.json()["access_token"]
    # Create
    response = end_to_end_client.post(
        "/authors/",
        json={"name": "Clarice Lispector"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "name": "clarice lispector"}
    # Update
    response = end_to_end_client.put(
        "/authors/1",
        json={"name": "manuel bandeira"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "manuel bandeira"}
    # Read by ID
    response = end_to_end_client.get("/authors/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "manuel bandeira"}
    # Delete
    response = end_to_end_client.delete(
        "/authors/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Author deleted"}
    # Get by query parameters
    names = (
        "Clarice Lispector",
        "Machado de Assis",
        "Robert C.  martin",
        "Mary Shelley",
    )
    ids = dict()
    for name in names:
        response = _post_author(end_to_end_client, name, token)
        ids[response.json()["name"]] = response.json()["id"]
    response = end_to_end_client.get("/authors?name=Ma&limit=2&offset=1")
    assert response.status_code == HTTPStatus.OK
    expected_author_names = ("robert c martin", "mary shelley")
    expected_authors = [
        {"id": ids[name], "name": name} for name in expected_author_names
    ]
    assert response.json() == {
        "limit": 2,
        "offset": 1,
        "total": 3,
        "name": "ma",
        "authors": expected_authors,
    }


@pytest.mark.end_to_end
def test_book_crud(end_to_end_client):
    # Prerequisite: Create user, login and create author
    # Create user
    end_to_end_client.post(
        "/users/",
        json={"username": "user", "email": "a@b.com", "password": "123"},
    )
    # Login
    response = end_to_end_client.post(
        "/auth/login", data={"username": "a@b.com", "password": "123"}
    )
    token = response.json()["access_token"]
    # Create author
    author = end_to_end_client.post(
        "/authors/",
        json={"name": "Andrew Hunt"},
        headers={"Authorization": f"Bearer {token}"},
    )
    author_id = author.json()["id"]
    # Create
    response = end_to_end_client.post(
        "/books/",
        json={"title": "The Pragmatic Programmer", "year": 1999, "author_id": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "the pragmatic programmer",
        "year": 1999,
        "author_id": author_id,
    }
    # Update
    response = end_to_end_client.patch(
        "/books/1", json={"year": 2000}, headers={"Authorization": f"Bearer {token}"}
    )
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
    response = end_to_end_client.delete(
        "/books/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Book deleted"}
    # Get by query parameters
    titles = (
        "The Pragmatic Programmer",
        "Clean Code",
        "Refactoring",
        "Clean Architecture",
    )
    ids = dict()
    for title in titles:
        response = end_to_end_client.post(
            "/books/",
            json={"title": title, "year": 2000, "author_id": author_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        ids[response.json()["title"]] = response.json()["id"]
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
                "id": ids["clean architecture"],
                "title": "clean architecture",
                "year": 2000,
                "author_id": author_id,
            },
        ],
    }


@pytest.mark.end_to_end
def test_user_crud(end_to_end_client):
    # Create
    response = end_to_end_client.post(
        "/users/",
        json={"username": " User ", "email": "a@b.com", "password": "password"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "username": "user", "email": "a@b.com"}
    # Login
    response = end_to_end_client.post(
        "/auth/login", data={"username": "a@b.com", "password": "password"}
    )
    token = response.json()["access_token"]
    # Update
    response = end_to_end_client.put(
        "/users/1",
        json={"username": " New User ", "email": "a@b.com", "password": "password"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "username": "new user", "email": "a@b.com"}
    # Read by ID
    response = end_to_end_client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "username": "new user", "email": "a@b.com"}
    # Delete
    response = end_to_end_client.delete(
        "/users/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}
    # Get by query parameters
    usernames = ("Alice", "Bob", "Charlie", "Diana", "Alan")
    ids = dict()
    for username in usernames:
        response = end_to_end_client.post(
            "/users/",
            json={
                "username": username,
                "email": f"{username.lower()}@email.com",
                "password": "password",
            },
        )
        ids[response.json()["username"]] = response.json()["id"]
    response = end_to_end_client.get("/users?username=Al&limit=2&offset=1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "limit": 2,
        "offset": 1,
        "total": 2,
        "username": "al",
        "email": None,
        "users": [
            {"id": ids["alan"], "username": "alan", "email": "alan@email.com"},
        ],
    }


@pytest.mark.end_to_end
def test_login(end_to_end_client):
    # Create user
    end_to_end_client.post(
        "/users/",
        json={"username": "user", "email": "a@b.com", "password": "123"},
    )
    # Login
    response = end_to_end_client.post(
        "/auth/login", data={"username": "a@b.com", "password": "123"}
    )
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


@pytest.mark.end_to_end
def test_refresh_token(end_to_end_client):
    # Create user
    end_to_end_client.post(
        "/users/",
        json={"username": "user", "email": "a@b.com", "password": "123"},
    )
    login_time = datetime(2021, 1, 1, 0, 0, 0)
    # Login
    with freeze_time(login_time):
        response = end_to_end_client.post(
            "/auth/login", data={"username": "a@b.com", "password": "123"}
        )
        refresh_token = response.json()["refresh_token"]

    # Refresh token
    access_expiration_minutes = Settings().ACCESS_TOKEN_EXPIRATION_MINUTES
    refresh_expiration_minutes = Settings().REFRESH_TOKEN_EXPIRATION_MINUTES
    valid_interval = (access_expiration_minutes + refresh_expiration_minutes) // 2
    new_time = login_time + timedelta(minutes=valid_interval)
    with freeze_time(new_time):
        response = end_to_end_client.post(
            "/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json()
        assert "refresh_token" not in response.json()
