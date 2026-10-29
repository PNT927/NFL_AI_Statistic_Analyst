def get_player_data(player_stats, player_name):
    player_data = player_stats[
        player_stats["player_display_name"] == player_name
    ]
    return player_data

def get_player_stat(player_stats, player_name, stat):
    player_data = get_player_data(player_stats, player_name)

    if player_data.empty:
        raise ValueError(f"Player {player_name} not found. Check the player's name and spelling.")

    if stat not in player_data.columns:
        raise ValueError(f"statistic '{stat}' is not supported. ")

    total = player_data[stat].sum()
    return total

def get_stat_leaders(player_stats, stat):
    if stat not in player_stats.columns:
        raise ValueError(f"statistic '{stat}' is not supported. ")

    leaders = (player_stats
               .groupby("player_display_name")[stat]
               .sum()
               .sort_values( ascending=False)
               .head(10)
               )
    return leaders

def get_recent_player_stats(player_stats, player_name, stat, num_games):
    player_data = get_player_data(player_stats, player_name)

    if player_data.empty:
        raise ValueError(f"Player '{player_name}' not found.")

    if stat not in player_stats.columns:
        raise ValueError(f"Statistic '{stat}' is not supported.")

    if num_games <= 0:
        raise ValueError("Number of games must be greater than zero.")

    recent_games = (player_data
                    .sort_values("week", ascending=False)
                    .head(num_games)
                    )

    total = recent_games[stat].sum()
    return total

def compare_players(player_stats, player1, player2, stat):
    player1_total = int(get_player_stat(player_stats, player1, stat))
    player2_total = int(get_player_stat(player_stats, player2, stat))

    difference = abs(player1_total - player2_total)

    if player1_total > player2_total:
        leader = player1

    elif player1_total == player2_total:
        leader = "Tie"

    else:
        leader = player2

    return {
        "player1": player1,
        "player1_total": player1_total,
        "player2": player2,
        "player2_total": player2_total,
        "stat": stat,
        "leader": leader,
        "difference": difference,
    }