
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.json()["status"] == "healthy"


def test_system_requires_auth():
    response = client.get("/system")
    assert response.status_code == 401
