
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

def get_recent_fantasy_performance(player_stats, player_name, num_games, scoring="standard"):

    # Filter player and regular-season games
    filt = (player_stats["player_display_name"] == player_name) & (player_stats["season_type"] == "REG")
    player_data = player_stats.loc[filt]

    # Validate inputs
    if player_data.empty:
        raise ValueError("Player not found in regular-season data.")

    if num_games <= 0:
        raise ValueError("Number of games must be greater than zero.")

    # Retrieve most recent games
    sorted_data = player_data.sort_values(by="week", ascending=False)
    recent_games = sorted_data.head(num_games)

    # Calculate fantasy points for each game
    fantasy_scores = []

    for index, row in recent_games.iterrows():
        game_stats = row.to_dict()
        points = calculate_fantasy_points(game_stats, scoring)
        fantasy_scores.append(points)

    # Calculate performance metrics
    total_points = sum(fantasy_scores)
    games_played = len(fantasy_scores)
    average_points = round(total_points / games_played, 2)

    # Return results
    result = {
        "player_name": player_name,
        "scoring": scoring,
        "games_played": games_played,
        "total_points": total_points,
        "average_points": average_points,
        "fantasy_scores": fantasy_scores
    }

    return result


if __name__ == "__main__":
    example_player = {
        "rushing_yards": 80,
        "rushing_tds": 1,
        "receptions": 4,
    }

    print(calculate_fantasy_points(example_player, "standard"))
    print(calculate_fantasy_points(example_player, "half_ppr"))
    print(calculate_fantasy_points(example_player, "ppr"))