import pandas as pd
from app.stats import (get_player_stat, get_stat_leaders,get_recent_player_stats, compare_players)
import pytest


def test_get_player_stat():
    player_stats = pd.DataFrame({
        "player_display_name": ["Bijan Robinson", "Bijan Robinson", "Jahmyr Gibbs"],
        "week": [1, 2, 1],
        "rushing_yards": [100, 85, 120]
    })

    result = get_player_stat(
        player_stats,
        "Bijan Robinson",
        "rushing_yards"
    )

    # Bijan has 100 + 85 = 185 rushing yards.
    # The test PASSES if the function returns 185.
    # The test FAILS if the function returns anything else.
    assert result == 185

# TEST 2: Check that an invalid player name is rejected.
def test_invalid_player():

    # Create a dataset containing only Bijan Robinson.
    player_stats = pd.DataFrame({
        "player_display_name": ["Bijan Robinson"],
        "rushing_yards": [100]
    })

    # We EXPECT a ValueError because "Fake Player" isn't in the dataset.
    # The test PASSES if the function raises ValueError.
    # The test FAILS if the function doesn't raise ValueError.
    with pytest.raises(ValueError):
        get_player_stat(
            player_stats,
            "Fake Player",
            "rushing_yards"
        )

# TEST 3: Check that players are ranked by total receiving yards.
def test_get_stat_leaders():

    # Create a small dataset with known receiving yard totals.
    player_stats = pd.DataFrame({
        "player_display_name": [
            "CeeDee Lamb",
            "Ja'Marr Chase",
            "CeeDee Lamb",
            "Justin Jefferson",
            "Ja'Marr Chase"
        ],
        "week": [1, 1, 2, 1, 2],
        "receiving_yards": [100, 150, 80, 120, 90]
    })

    # Call our leaderboard function.
    leaders = get_stat_leaders(player_stats, "receiving_yards")
    # Check that Ja'Marr Chase is first with 240 yards.
    assert leaders.index[0] == "Ja'Marr Chase"
    assert leaders.iloc[0] == 240

    # Check that CeeDee Lamb is second with 180 yards.
    assert leaders.index[1] == "CeeDee Lamb"
    assert leaders.iloc[1] == 180

# TEST 4: Check that an unsupported statistic is rejected.
def test_invalid_leaderboard_stat():

    # Create a small dataset containing only rushing yards.
    player_stats = pd.DataFrame({
        "player_display_name": ["Bijan Robinson"],
        "rushing_yards": [100]
    })

    # We expect the function to raise a ValueError.
    # The test passes if the expected error occurs.
    with pytest.raises(ValueError):
        get_stat_leaders(player_stats, "flying_yards")

# TEST 5: Check passing yards across a player's two most recent games.
def test_get_recent_player_stats():

    # Create four weeks of sample passing statistics.
    player_stats = pd.DataFrame({
        "player_display_name": [
            "Patrick Mahomes",
            "Patrick Mahomes",
            "Patrick Mahomes",
            "Patrick Mahomes"
        ],
        "week": [1, 2, 3, 4],
        "passing_yards": [250, 300, 275, 325]
    })

    # Calculate passing yards from the two most recent games.
    result = get_recent_player_stats(
        player_stats,
        "Patrick Mahomes",
        "passing_yards",
        2
    )

    # Check that weeks 4 and 3 add up to 600 yards.
    assert result == 600

# TEST 6: Check that two players are compared correctly.
def test_compare_players():

    # Create a dataset with two weeks of rushing statistics.
    player_stats = pd.DataFrame({
        "player_display_name": [
            "Bijan Robinson",
            "Jahmyr Gibbs",
            "Bijan Robinson",
            "Jahmyr Gibbs"
        ],
        "week": [1, 1, 2, 2],
        "rushing_yards": [120, 90, 85, 110]
    })

    # Compare both players' total rushing yards.
    result = compare_players(
        player_stats,
        "Bijan Robinson",
        "Jahmyr Gibbs",
        "rushing_yards"
    )

    assert result["player1_total"] == 205
    assert result["player2_total"] == 200
    # Check that Bijan Robinson is the leader.
    assert result["leader"] == "Bijan Robinson"

    # Check that the difference is 5 yards.
    assert result["difference"] == 5