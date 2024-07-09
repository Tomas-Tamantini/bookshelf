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