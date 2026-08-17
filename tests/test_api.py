from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200


def test_simulate():
    response = client.get("/simulate")

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert "passed_tests" in data
    assert "failed_tests" in data
    assert "average_score" in data