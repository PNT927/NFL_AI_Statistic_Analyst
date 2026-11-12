from fastapi import FastAPI, HTTPException
import nflreadpy as nfl

from app.stats import get_player_stat
from app.fantasy import calculate_fantasy_points
app = FastAPI(title="NFL Statistics Analyst API")

# Load the 2026 NFL player statistics
player_stats = nfl.load_player_stats([2026]).to_pandas()


@app.get("/")
def home():
    return {"message": "NFL Statistics Analyst API is running"}


@app.get("/players/{player_name}/stats/{stat}")
def player_stat(player_name: str, stat: str):
    try:
        total = get_player_stat(player_stats, player_name, stat)

        return {
            "player": player_name,
            "stat": stat,
            "value": float(total),
            "season": 2026
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@app.get("/players/{player_name}/fantasy/{scoring}/{week}")
def fantasy(player_name: str, scoring: str, week: int):

    # Remove accidental spaces at beginning or end
    player_name = player_name.strip()

    # Find the player's statistics for the selected week
    player = player_stats[
        (player_stats["player_display_name"] == player_name)
        & (player_stats["week"] == week)
        & (player_stats["season_type"] == "REG")
        ]

    # Check whether the player was found
    if player.empty:
        raise HTTPException(
            status_code=404,
            detail="Player not found for the selected week"
        )

    # Convert the player's statistics into a dictionary
    player_data = player.iloc[0].to_dict()

    # Calculate fantasy points and handle invalid scoring formats
    try:
        points = calculate_fantasy_points(player_data, scoring)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    # Return the result as JSON
    return {
        "player": player_name,
        "week": week,
        "scoring": scoring,
        "fantasy_points": points
    }