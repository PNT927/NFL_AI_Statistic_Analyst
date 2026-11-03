from fastapi import FastAPI, HTTPException
import nflreadpy as nfl

from app.stats import get_player_stat

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