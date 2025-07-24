# scripts/groq_response.py

import requests
from app.config import GROQ_API_KEY  # Centralized env variable

def generate_summary_from_gpt(query, prompt_type="bio"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Choose the system prompt based on use case
    if prompt_type == "bio":
        system_prompt = "You are a helpful and expert sports analyst."
        user_prompt = f"Write a short professional biography of the sports player named {query}."
    elif prompt_type == "qa":
        system_prompt = "You are a helpful and expert sports analyst who answers user questions about sports."
        user_prompt = query
    else:
        system_prompt = "You are a helpful AI."
        user_prompt = query

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
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
