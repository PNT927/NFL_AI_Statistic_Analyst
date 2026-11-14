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


def test_recent_fantasy_performance_endpoint():
    response = client.get(
        "/players/Bijan%20Robinson/fantasy/ppr/recent/3"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["player_name"] == "Bijan Robinson"
    assert data["scoring"] == "ppr"
    assert data["games_played"] == 3
    assert len(data["fantasy_scores"]) == 3
    assert data["total_points"] == sum(data["fantasy_scores"])
    assert data["average_points"] == round(data["total_points"] / 3, 2)


def test_recent_fantasy_endpoint_invalid_player():
    response = client.get(
        "/players/Unknown%20Player/fantasy/ppr/recent/3"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Player not found in regular-season data."


def test_recent_fantasy_endpoint_invalid_game_count():
    response = client.get(
        "/players/Bijan%20Robinson/fantasy/ppr/recent/0"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Number of games must be greater than zero."


def test_recent_fantasy_endpoint_invalid_scoring():
    response = client.get(
        "/players/Bijan%20Robinson/fantasy/invalid/recent/3"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported scoring format"