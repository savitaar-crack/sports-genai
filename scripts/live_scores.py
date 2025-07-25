import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load keys
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")
SPORTSMONKS_API_KEY = os.getenv("SPORTSMONKS_API_KEY")

def get_live_football_scores():
    try:
        if not FOOTBALL_API_KEY:
            raise ValueError("FOOTBALL_API_KEY not set in .env")

        url = "https://api.football-data.org/v4/matches?status=LIVE"
        headers = {"X-Auth-Token": FOOTBALL_API_KEY}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("⚠️ Football API Error:", response.text)
            return []

        data = response.json()
        matches = data.get("matches", [])

        # Optional: Print some sample match data
        print("⚽ Football Live Matches Fetched:", len(matches))

        # Simplify for main.py
        results = []
        for match in matches:
            results.append({
                "homeTeam": match["homeTeam"]["name"],
                "awayTeam": match["awayTeam"]["name"],
                "score": match["score"]
            })
        return results

    except Exception as e:
        print("❌ Error fetching football scores:", e)
        return []

def get_live_cricket_scores():
    try:
        if not SPORTSMONKS_API_KEY:
            raise ValueError("SPORTSMONKS_API_KEY not set in .env")

        url = "https://cricket.sportmonks.com/api/v2.0/livescores"
        params = {"api_token": SPORTSMONKS_API_KEY}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("⚠️ Cricket API Error:", response.text)
            return []

        data = response.json()
        matches = data.get("data", [])

        # Optional: Print match count
        print("🏏 Cricket Live Matches Fetched:", len(matches))

        # Simplify structure
        results = []
        for match in matches:
            scores = match.get("scoreboards", [])
            simplified_scores = [{
                "inning": s.get("inning"),
                "runs": s.get("total", 0),
                "wickets": s.get("wickets", 0)
            } for s in scores] if scores else []

            results.append({
                "name": match.get("name", "Match"),
                "status": match.get("status", "Unknown"),
                "score": simplified_scores
            })

        return results

    except Exception as e:
        print("❌ Error fetching cricket scores:", e)
        return []
