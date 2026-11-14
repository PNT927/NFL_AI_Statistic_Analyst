
import nflreadpy as nfl

player_stats = nfl.load_player_stats([2026]).to_pandas()

print("Total rows:", len(player_stats))

print("\nFantasy-related columns:")
keywords = (
    "passing", "rushing", "receiving",
    "receptions", "interceptions",
    "fumbles", "two_point"
)

for column in player_stats.columns:
    if any(keyword in column for keyword in keywords):
        print(column)

print("\nSample player:")
print(
    player_stats[
        player_stats["player_display_name"] == "Bijan Robinson"
    ].head(3).to_string(index=False)
)
