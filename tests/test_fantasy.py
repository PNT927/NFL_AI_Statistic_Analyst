
import pytest

from app.fantasy import calculate_fantasy_points


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
