import pandas as pd
import pytest

from app.fantasy import calculate_fantasy_points, get_recent_fantasy_performance


def test_standard_scoring():
    player = {
        "rushing_yards": 80,
        "rushing_tds": 1,
        "receptions": 4,
    }

    assert calculate_fantasy_points(player, "standard") == 14.0


def test_half_ppr_scoring():
    player = {
        "rushing_yards": 80,
        "rushing_tds": 1,
        "receptions": 4,
    }

    assert calculate_fantasy_points(player, "half_ppr") == 16.0


def test_full_ppr_scoring():
    player = {
        "rushing_yards": 120,
        "rushing_tds": 2,
        "receptions": 5,
    }

    assert calculate_fantasy_points(player, "ppr") == 29.0


def test_invalid_scoring_format():
    player = {"rushing_yards": 100}

    with pytest.raises(ValueError):
        calculate_fantasy_points(player, "super_ppr")


def test_missing_statistics():
    player = {"rushing_yards": 50}

    assert calculate_fantasy_points(player) == 5.0


def test_get_recent_fantasy_performance():
    player_stats = pd.DataFrame({
        "player_display_name" : ["Test Player","Test Player","Test Player"],
        "season_type" : ["REG","REG","REG"],
        "week" : [1,2,3],
        "rushing_yards" : [100,80,120],
        "rushing_tds": [1,0,1],
    })


def test_recent_fantasy_insufficient_games():
    player_stats = pd.DataFrame({
        "player_display_name": ["Test Player"],
        "season_type": ["REG"],
        "week": [1],
        "rushing_yards": [100],
        "rushing_tds": [1],
    })

    result = get_recent_fantasy_performance(
        player_stats, "Test Player", 5
    )

    assert result["games_played"] == 1
    assert result["total_points"] == 16.0
    assert result["average_points"] == 16.0

def test_recent_fantasy_insufficient_games():
        player_stats = pd.DataFrame({
            "player_display_name": ["Test Player"],
            "season_type": ["REG"],
            "week": [1],
            "rushing_yards": [100],
            "rushing_tds": [1],
        })

        result = get_recent_fantasy_performance(
            player_stats, "Test Player", 5
        )

        assert result["games_played"] == 1
        assert result["total_points"] == 16.0
        assert result["average_points"] == 16.0


def test_recent_fantasy_regular_season_only():
    player_stats = pd.DataFrame({
        "player_display_name": ["Test Player", "Test Player"],
        "season_type": ["REG", "POST"],
        "week": [18, 19],
        "rushing_yards": [100, 200],
        "rushing_tds": [1, 2],
    })

    result = get_recent_fantasy_performance(
        player_stats, "Test Player", 2
    )

    assert result["games_played"] == 1
    assert result["total_points"] == 16.0

def test_recent_fantasy_ppr():
    player_stats = pd.DataFrame({
        "player_display_name": ["Test Player"],
        "season_type": ["REG"],
        "week": [1],
        "receiving_yards": [100],
        "receptions": [5],
        "receiving_tds": [1],
    })

    result = get_recent_fantasy_performance(
        player_stats, "Test Player", 1, "ppr"
    )

    assert result["total_points"] == 21.0
    assert result["average_points"] == 21.0

def test_recent_fantasy_invalid_scoring():
    player_stats = pd.DataFrame({
        "player_display_name": ["Test Player"],
        "season_type": ["REG"],
        "week": [1],
        "rushing_yards": [100],
    })

    with pytest.raises(ValueError):
        get_recent_fantasy_performance(
            player_stats, "Test Player", 1, "invalid"
        )

def test_recent_fantasy_invalid_game_count():
    player_stats = pd.DataFrame({
        "player_display_name": ["Test Player"],
        "season_type": ["REG"],
        "week": [1],
        "rushing_yards": [100],
        "rushing_tds": [1],
    })

    with pytest.raises(ValueError, match="Number of games must be greater than zero"):
        get_recent_fantasy_performance(
            player_stats, "Test Player", 0, "standard"
        )


def test_recent_fantasy_invalid_player():
    player_stats = pd.DataFrame({
        "player_display_name": ["Test Player"],
        "season_type": ["REG"],
        "week": [1],
        "rushing_yards": [100],
        "rushing_tds": [1],
    })

    with pytest.raises(ValueError, match="Player not found in regular-season data"):
        get_recent_fantasy_performance(
            player_stats, "Unknown Player", 1, "standard"
        )

