def get_player_data(player_stats, player_name):
    player_data = player_stats[
        player_stats["player_display_name"] == player_name
    ]
    return player_data

def get_player_stat(player_stats, player_name, stat):
    player_data = get_player_data(player_stats, player_name)
    total = player_data[stat].sum()
    return total