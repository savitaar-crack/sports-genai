# test_huggingface_api.py

import os
import requests
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
hf_token = os.getenv("HUGGINGFACE_API_KEY")

headers = {
    "Authorization": f"Bearer {hf_token}"
}

# ✅ Free HF inference-compatible model
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

prompt = "Write a short biography of Lionel Messi in 100 words."

result = query({"inputs": prompt})
if result:
    print("✅ Response:", result[0]["generated_text"])
