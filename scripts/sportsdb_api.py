# scripts/sportsdb_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("THESPORTSDB_API_KEY")

BASE_URL = "https://www.thesportsdb.com/api/v1/json"

def search_player(player_name):
    url = f"{BASE_URL}/{API_KEY}/searchplayers.php?p={player_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["player"]:
            return data["player"][0]  # Return first match
    return None
