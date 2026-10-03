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
    leaders = (player_stats
               .groupby("player_display_name")[stat]
               .sum()
               .sort_values( ascending=False)
               .head(10)
               )

    if stat not in player_stats.columns:
        raise ValueError(f"statistic '{stat}' is not supported. ")

    return leaders


