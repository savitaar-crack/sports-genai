# scripts/live_scores.py

import os
import requests
from pycricbuzz import Cricbuzz
from dotenv import load_dotenv

load_dotenv()

FOOTBALL_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

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

# --- Cricket Scores via Cricbuzz (no API key)
def get_live_cricket_scores():
    c = Cricbuzz()
    try:
        matches = c.matches()
        live_scores = []
        for match in matches:
            if match['mchstate'] == 'inprogress':
                match_id = match['id']
                score_details = c.livescore(match_id)
                match_info = {
                    "name": match['team1']['name'] + " vs " + match['team2']['name'],
                    "status": match['status'],
                    "score": score_details.get('score', [])
                }
                live_scores.append(match_info)
        return live_scores
    except Exception as e:
        print("⚠️ Cricbuzz error:", e)
        return []
