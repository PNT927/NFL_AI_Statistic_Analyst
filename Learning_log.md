# NFL Statistics Analyst — Learning Log

## Project Goal
Develop an AI-powered NFL statistics and fantasy analysis application using Python, real NFL data, FastAPI and eventually LLM tool calling.

## Sessions 1–3: Statistics Engine and Testing

**Built**
- Functions to retrieve player statistics, identify statistical leaders, calculate recent-game totals and compare players.
- Initial automated tests using pytest.

**Learned**
- Filtering, grouping and aggregating data.
- Using `assert` to verify results.
- Using `pytest.raises()` to check expected errors.
- The importance of validating inputs before processing them.

**CV value:** Developed reusable Python functions for analysing NFL player statistics and introduced automated unit testing.

## Session 4: Validation and Edge Cases — Completed

**Built**
- Additional tests for invalid inputs, tied players and different comparison outcomes.

**Learned**
- Boundary conditions such as `num_games <= 0`.
- Dictionary keys versus variables.
- The difference between application validation and testing.

**Verified**
- 10/10 pytest tests passed.
- Changes committed and pushed to GitHub.
- Commit: `ea075a5`.

**CV value:** Expanded automated test coverage for normal and edge-case behaviour using pytest.

## Session 5: FastAPI and Real NFL Data — In Progress

**Built**
- Created `app/api.py`.
- Implemented a home endpoint and a player-statistics endpoint.
- Integrated real 2026 NFL statistics using `nflreadpy`.
- Connected FastAPI to the existing `get_player_stat()` function.
- Implemented HTTP error handling.

**Learned**
- API: Allows software applications to communicate.
- Endpoint: A URL route that exposes functionality.
- GET: HTTP method used to request information.
- JSON: Structured format for exchanging data.
- Uvicorn: Runs the FastAPI application.
- HTTP 400: Indicates an invalid request.

**Verified**
- Loaded 8,428 NFL player-statistic records.
- Retrieved Patrick Mahomes' passing yards from the loaded dataset.
- Successfully accessed the Swagger documentation at `/docs`.
- Confirmed invalid player names and statistics produce the expected error responses.

**Problems and Solutions**
- FastAPI and Uvicorn were initially missing. Installed them into the project's virtual environment and verified their installation.

**CV value:** Developed REST API endpoints using FastAPI to expose real NFL player statistics through JSON responses, including input validation and error handling.

**Remaining Tasks**
- Add automated FastAPI endpoint tests.
- Update `requirements.txt`.
- Review and commit Session 5 changes.

## Future Sessions

- Fantasy scoring
- Recent performance analysis
- Opponent matchup analysis
- Fantasy player comparisons
- AI integration
- Web interface
- Data refresh, testing and deployment

## Session 6 — NFL Fantasy Scoring Engine

### What I built
- Developed `app/fantasy.py` to calculate NFL fantasy points.
- Implemented standard, half-PPR and full-PPR scoring.
- Integrated real 2026 NFL statistics using nflreadpy and Pandas.
- Added a FastAPI endpoint to calculate weekly player fantasy points.
- Created automated tests for scoring calculations and API responses.

### Python concepts learned
- Dictionaries and key-value pairs.
- Functions, parameters and return values.
- For loops and conditional statements.
- `.get()`, `.copy()`, `.strip()`, `.iloc[0]` and `.to_dict()`.
- Pandas DataFrame filtering.
- Error handling using `try/except`.
- API endpoints, JSON responses and HTTP status codes.
- Automated testing using pytest.

### Problems solved
- Corrected mismatched dataset column names.
- Used `fumbles_lost_total` to avoid double-counting turnovers.
- Fixed a player lookup issue caused by trailing whitespace.
- Implemented appropriate HTTP responses for invalid requests.

### Verification
- Bijan Robinson Week 1 PPR: 31.3 calculated points.
- Dataset reference: 31.3 points.
- Swagger API requests returned the expected 200, 400 and 404 statuses.
- All 21 automated tests passed.
- One non-blocking dependency deprecation warning remains.

### What I should remember
The API receives a request, filters the dataset, converts the selected player record into a dictionary, passes it to the scoring function and returns the result as JSON.

Automated tests verify that the application behaves correctly for both valid and invalid inputs.