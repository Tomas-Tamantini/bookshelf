from http import HTTPStatus


def test_health_check_returns_no_content(client):
    response = client.get("/health")
    assert response.status_code == HTTPStatus.NO_CONTENT
