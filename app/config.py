# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Constants accessible throughout the app
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# You can add more configs here as needed
PROJECT_NAME = "Sports GenAI"
# Configs and API keys will go here
