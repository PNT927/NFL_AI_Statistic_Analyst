from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "NFL Statistics Analyst API is running"
    }


def test_invalid_player_endpoint():
    response = client.get(
        "/players/Fake%20Player/stats/passing_yards"
    )

    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


def test_invalid_stat_endpoint():
    response = client.get(
        "/players/Patrick%20Mahomes/stats/flying_yards"
    )

    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]