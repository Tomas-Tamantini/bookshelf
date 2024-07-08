from http import HTTPStatus

import pytest


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
