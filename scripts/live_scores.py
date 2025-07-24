# scripts/live_scores.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# --- API Keys from .env or directly used here
FOOTBALL_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
SPORTSMONK_API_TOKEN = os.getenv("SPORTSMONK_API_TOKEN", "kTfdEPvLa0ms1V3GeXBAj8cWvPi1ksxaY2KKZfEhSlo1pdNYFc5vF941bkMA")

# --- Football Scores via Football-Data.org
def get_live_football_scores():
    url = "https://api.football-data.org/v4/matches?status=LIVE"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            live_matches = []
            for match in data.get("matches", []):
                live_matches.append({
                    "homeTeam": match["homeTeam"]["name"],
                    "awayTeam": match["awayTeam"]["name"],
                    "score": match["score"],
                    "utcDate": match["utcDate"],
                    "status": match["status"]
                })
            return live_matches
        else:
            print("⚠️ Football API Error:", response.text)
            return []
    except Exception as e:
        print("⚠️ Football API Exception:", e)
        return []

# --- Cricket Scores via SportsMonks API
def get_live_cricket_scores():
    base_url = "https://cricket.sportmonks.com/api/v2.0/livescores"
    params = {
        "api_token": SPORTSMONK_API_TOKEN,
        "include": "localteam,visitorteam,runs,scoreboards"
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            matches = data.get("data", [])
            live_scores = []

            for match in matches:
                local_team = match.get("localteam", {}).get("name", "Team A")
                visitor_team = match.get("visitorteam", {}).get("name", "Team B")
                status = match.get("status", "N/A")
                overs = "-"
                runs = "-"
                wickets = "-"

                # Score info
                runs_data = match.get("runs", [])
                if runs_data:
                    for team_score in runs_data:
                        if team_score.get("team_id") == match.get("localteam_id"):
                            local_runs = team_score.get("score", 0)
                            local_wickets = team_score.get("wickets", 0)
                            local_overs = team_score.get("overs", 0)
                        elif team_score.get("team_id") == match.get("visitorteam_id"):
                            visitor_runs = team_score.get("score", 0)
                            visitor_wickets = team_score.get("wickets", 0)
                            visitor_overs = team_score.get("overs", 0)

                    score_str = f"{local_team}: {local_runs}/{local_wickets} ({local_overs} ov), {visitor_team}: {visitor_runs}/{visitor_wickets} ({visitor_overs} ov)"
                else:
                    score_str = f"{local_team} vs {visitor_team} (No score yet)"

                live_scores.append({
                    "name": f"{local_team} vs {visitor_team}",
                    "status": status,
                    "score": score_str
                })

            return live_scores
        else:
            print("⚠️ SportsMonks API Error:", response.text)
            return []
    except Exception as e:
        print("⚠️ SportsMonks Exception:", e)
        return []
