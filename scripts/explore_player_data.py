import nflreadpy as nfl
from app.stats import get_player_stat

current_season = nfl.get_current_season()

player_stats_polars = nfl.load_player_stats([current_season])
player_stats = player_stats_polars.to_pandas()

important_columns = [
    "player_id",
    "player_display_name",
    "position",
    "season",
    "week",
    "season_type",
    "team",
    "opponent_team",
    "passing_yards",
    "passing_tds",
    "carries",
    "rushing_yards",
    "receptions",
    "receiving_yards",
    "def_tackles_solo",
    "def_sacks",
]

print(f"Current season: {current_season}")
print(f"Dataset type: {type(player_stats)}")
print(f"Rows and columns: {player_stats.shape}")
print(f"Latest available week: {player_stats['week'].max()}")

print(player_stats[important_columns].head(10).to_string(index=False))

player_name = "Bijan Robinson"
stat = "rushing_yards"
result = get_player_stat(player_stats, player_name, stat)
print(f"\n {player_name} {stat}: {result}")