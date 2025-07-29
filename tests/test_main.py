import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à Visualize API!"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("src.main.httpx.AsyncClient.get", new_callable=AsyncMock)
def test_apod_success(mock_get):
    mock_data = {
        "title": "Test APOD",
        "explanation": "Example",
        "url": "http://example.com/image.jpg"
    }

    class MockResponse:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            return mock_data

    mock_get.return_value = MockResponse()

    response = client.get("/apod")
    assert response.status_code == 200
    assert response.json() == mock_data

