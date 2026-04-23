"""Tests for API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

import app.api as api_module


@pytest.fixture()
def api_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """TestClient with RabbitMQ side-effects disabled."""

    def _noop_send_to_queue(_: dict) -> None:
        return None

    monkeypatch.setattr(api_module, "send_to_queue", _noop_send_to_queue)
    api_module.app.state.click_count = 0
    return TestClient(api_module.app)


def test_health(api_client: TestClient) -> None:
    """Health endpoint returns a stable payload."""
    response = api_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Healthy"}


def test_home_html(api_client: TestClient) -> None:
    """Home page returns HTML content."""
    response = api_client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Mini Web App" in response.text


def test_click_returns_payload_and_increments_count(api_client: TestClient) -> None:
    """Click endpoint echoes payload and increments click count."""
    payload = {"source": "test", "robot": "simple-google"}
    response = api_client.post("/api/click", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["robot"] == "simple-google"
    assert body["payload"] == payload
    assert body["click_count"] == 1

    response2 = api_client.post("/api/click", json=payload)
    assert response2.status_code == 200
    assert response2.json()["click_count"] == 2
