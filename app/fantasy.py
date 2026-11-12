
SCORING_RULES = {
    "passing_yards": 0.04,
    "passing_tds": 4,
    "passing_interceptions": -2,
    "rushing_yards": 0.1,
    "rushing_tds": 6,
    "receiving_yards": 0.1,
    "receiving_tds": 6,
    "receptions": 0,
    "fumbles_lost_total": -2,
    "passing_2pt_conversions": 2,
    "rushing_2pt_conversions": 2,
    "receiving_2pt_conversions": 2,
}



def calculate_fantasy_points(player_stats: dict, scoring: str = "standard") -> float:
    if scoring not in ("standard", "half_ppr", "ppr"):
        raise ValueError("Unsupported scoring format")

    rules = SCORING_RULES.copy()

    if scoring == "half_ppr":
        rules["receptions"] = 0.5
    elif scoring == "ppr":
        rules["receptions"] = 1

    total = 0.0

    for stat, points_per_unit in rules.items():
        value = player_stats.get(stat, 0)
        total += value * points_per_unit

    return round(total, 2)


if __name__ == "__main__":
    example_player = {
        "rushing_yards": 80,
        "rushing_tds": 1,
        "receptions": 4,
    }

    print(calculate_fantasy_points(example_player, "standard"))
    print(calculate_fantasy_points(example_player, "half_ppr"))
    print(calculate_fantasy_points(example_player, "ppr"))