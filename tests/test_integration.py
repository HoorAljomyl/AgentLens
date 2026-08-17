from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_full_evaluation_flow():
    response = client.get("/simulate")

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert len(data["results"]) > 0

    for result in data["results"]:
        assert "user" in result
        assert "personality" in result
        assert "message" in result
        assert "response" in result

        assert "passed" in result
        assert "score" in result
        assert 0 <= result["score"] <= 100

        assert "failure_type" in result
        assert "recommendation" in result
        assert "llm_judgment" in result

        assert "trace" in result
        assert "steps" in result["trace"]
        assert len(result["trace"]["steps"]) > 0