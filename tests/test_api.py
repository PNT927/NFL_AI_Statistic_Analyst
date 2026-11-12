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


def test_fantasy_ppr_success():
    response = client.get(
        "/players/Bijan%20Robinson/fantasy/ppr/1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["player"] == "Bijan Robinson"
    assert data["week"] == 1
    assert data["scoring"] == "ppr"
    assert data["fantasy_points"] == 31.3


def test_fantasy_invalid_scoring():
    response = client.get(
        "/players/Bijan%20Robinson/fantasy/super_ppr/1"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported scoring format"


def test_fantasy_player_not_found():
    response = client.get(
        "/players/Random%20Player/fantasy/ppr/1"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found for the selected week"
