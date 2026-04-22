"""Test API endpoints"""

import random
import os
from fastapi.testclient import TestClient
from app.api import app, leak

client = TestClient(app)
TOKEN_FIXO = os.getenv("TOKEN_FIXO")


def test_health():
    """
    Test health endpoint
    """
    response = client.get("/health", headers={"x-token": TOKEN_FIXO})

    assert response.status_code == 200
    assert response.json() == {"message": "Healthy"}


def test_slow():
    """
    Test slow endpoint
    """
    ms = 1000
    response = client.get(f"/slow?ms={ms}", headers={"x-token": TOKEN_FIXO})

    assert response.status_code == 200
    assert response.json() == {"message": f"Slow {ms}ms completed"}


def test_compute():
    """
    Test compute endpoint
    """
    response = client.get("/compute", headers={"x-token": TOKEN_FIXO})

    assert response.status_code == 200
    assert response.json() == {"message": "Computation completed"}


def test_memory_leak():
    """
    Test memory leak endpoint
    """

    leak.clear()
    response = client.get("/leak", headers={"x-token": TOKEN_FIXO})

    assert response.status_code == 200
    assert response.json() == {"size": 1}


def test_random_error(monkeypatch):
    """
    Test random error endpoint
    """

    monkeypatch.setattr(random, "random", lambda: 1.0)
    response = client.get("/random-error", headers={"x-token": TOKEN_FIXO})

    assert response.status_code == 200
    assert response.json() == {"message": "No error"}
