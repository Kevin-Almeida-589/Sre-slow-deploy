"""Test API endpoints"""

from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_health():
    """
    Test health endpoint
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Healthy"}


def test_home_html():
    """
    Test home page returns HTML.
    """
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Mini Web App" in response.text


def test_click():
    """
    Test click endpoint
    """
    response = client.post("/api/click", json={"source": "test", "robot": "Simple-google"})

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["robot"] == "Simple-google"
    assert body["payload"] == {"source": "test", "robot": "Simple-google"}
