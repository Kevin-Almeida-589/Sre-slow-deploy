"""Tests for API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

import app.api as api_module


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """TestClient with RabbitMQ side-effects disabled."""

    def _noop_send_to_queue(_: dict) -> None:
        return None

    monkeypatch.setattr(api_module, "send_to_queue", _noop_send_to_queue)
    api_module._click_count = 0  # pylint: disable=protected-access
    return TestClient(api_module.app)


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "Healthy"}


def test_home_html(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Mini Web App" in response.text


def test_click_returns_payload_and_increments_count(client: TestClient) -> None:
    payload = {"source": "test", "robot": "simple-google"}
    response = client.post("/api/click", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["robot"] == "simple-google"
    assert body["payload"] == payload
    assert body["click_count"] == 1

    response2 = client.post("/api/click", json=payload)
    assert response2.status_code == 200
    assert response2.json()["click_count"] == 2
