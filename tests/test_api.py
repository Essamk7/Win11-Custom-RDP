from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_system_requires_key():
    response = client.get("/system")
    assert response.status_code == 401


def test_system_with_key(monkeypatch):
    monkeypatch.setattr("app.main._api_key", "test-key")

    response = client.get(
        "/system",
        headers={"X-API-Key": "test-key"}
    )

    assert response.status_code == 200
    assert "architecture" in response.json()
