import nflreadpy as nfl

from app.fantasy import calculate_fantasy_points

df = nfl.load_player_stats([2026]).to_pandas()

player = df[
    (df["player_display_name"] == "Bijan Robinson")
    & (df["week"] == 1)
    & (df["season_type"] == "REG")
]

if player.empty:
    raise ValueError("Player data not found")

player_stats = player.iloc[0].to_dict()

calculated = calculate_fantasy_points(player_stats, "ppr")
dataset_points = player_stats["fantasy_points_ppr"]

print("Player: Bijan Robinson")
print("Week:", player_stats["week"])
print("Our calculated points:", calculated)
print("Dataset PPR points:", dataset_points)
print("Match:", abs(calculated - dataset_points) < 0.01)
