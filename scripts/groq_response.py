# scripts/gpt_response.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def generate_summary_from_gpt(player_name):
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",  # Updated model
        "messages": [
            {"role": "system", "content": "You are a helpful and expert sports analyst."},
            {"role": "user", "content": f"Write a short professional biography of the sports player named {player_name}."}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            print(f"❌ Groq API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print("❌ Groq API Exception:", e)
        return None
