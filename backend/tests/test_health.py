"""Health endpoint test."""
import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.mark.unit
def test_health_returns_ok(client: TestClient):
    """Health check returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "multi-school-api"
