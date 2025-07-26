import sys
import os
from dotenv import load_dotenv
import streamlit as st

# Ensure proper module import from /scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.live_scores import get_live_football_scores, get_live_cricket_scores
from scripts.ingest_news import fetch_espn_news
from scripts.sportsdb_api import search_player
from scripts.groq_response import generate_summary_from_gpt

# --- Load Environment ---
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

# --- Page Config ---
st.set_page_config(page_title="⚽ Sports GenAI", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .news-card {
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: #f8f9fa;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }
        .score-card {
            background-color: #f0f9ff;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border: 1px solid #00B4D8;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        }
        h1, h2, h3, h4 {
            color: #0077b6;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown("<h1 style='text-align: center;'>⚽ Sports GenAI Hub</h1><hr>", unsafe_allow_html=True)

# --- Section 1: Groq Q&A ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Ask About Any Match, Event or Player")
    general_question = st.text_input("Ask me anything about sports...")

    if general_question:
        with st.spinner("🤔 Thinking..."):
            if groq_key:
                answer = generate_summary_from_gpt(general_question, prompt_type="qa")
                if answer:
                    st.success(answer)
                else:
                    st.error("❌ Groq couldn't generate a response.")
            else:
                st.error("❌ GROQ_API_KEY missing in your .env file.")

with col2:
    st.markdown("### 🤖 Powered by Groq GenAI")
    st.caption("This app uses Groq (Mixtral) to summarize and answer queries.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Groq_logo_2023.svg/512px-Groq_logo_2023.svg.png", width=150)

# --- Section 2: Player Lookup ---
st.markdown("---")
st.markdown("<h3>🔎 Player Lookup</h3>", unsafe_allow_html=True)

player_name = st.text_input("Enter a player’s full name:")

if player_name:
    st.write(f"Searching info for: {player_name}")
    player = search_player(player_name)

    if player:
        name = player.get("strPlayer", "Unknown")
        position = player.get("strPosition", "N/A")
        nationality = player.get("strNationality", "N/A")

        st.markdown(f"""
        <div class="score-card">
            <h3>{name}</h3>
            <p><strong>Position:</strong> {position} | <strong>Nationality:</strong> {nationality}</p>
        </div>
        """, unsafe_allow_html=True)

        image = player.get("strCutout") or player.get("strThumb")
        if image:
            st.image(image, width=250)

        description = player.get("strDescriptionEN")
        if description:
            st.markdown(description[:500] + "...")
        else:
            st.warning("⚠️ No biography found. Generating one using AI...")
            if groq_key:
                ai_bio = generate_summary_from_gpt(player_name)
                if ai_bio:
                    st.markdown(ai_bio)
                else:
                    st.error("❌ Groq failed to generate a biography.")
            else:
                st.error("❌ GROQ_API_KEY missing in your .env file.")
    else:
        st.warning("❌ Player not found. Try using full name like 'Virat Kohli' or 'Cristiano Ronaldo'.")

# --- Section 3: News Feed ---
st.markdown("---")
st.subheader("📰 Top Sports Headlines (Live from ESPN)")

news_items = fetch_espn_news(limit=5)
for item in news_items:
    st.markdown(f"""
    <div class="news-card">
        <h4><a href="{item['link']}" target="_blank">{item['title']}</a></h4>
        <p style="color:gray;">{item['summary']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- Section4: Live Scores ---
st.markdown("---")
st.subheader(" Live Scores")

try:
    with st.expander(" Live Football Matches"):
        football_matches = get_live_football_scores()
        if football_matches:
            for match in football_matches[:5]:
                home = match.get("homeTeam")
                away = match.get("awayTeam")
                full_time = match.get("score", {}).get("fullTime")
                if home and away and full_time:
                    st.markdown(
                        f"**{home} {full_time.get('home',0)} - {full_time.get('away',0)} {away}**"
                    )
                else:
                    st.info("No live football matches at the moment or failed to fetch.")
except Exception as e:
    st.error(f"Error fetching live football scores: {e}")

try:
    with st.expander(" Live Cricket Matches"):
        cricket_matches = get_live_cricket_scores()
        if cricket_matches:
            for match in cricket_matches[:5]:
                name = match.get("name", "Match")
                status = match.get("status", "Unknown")
                score = match.get("score", [])
                if name and status and score:
                    score_summary = " | ".join([
                        f"{s.get('inning', '')}: {s.get('runs', '')}/{s.get('wickets', '')}" for s in score
                    ]) if score else "No score yet"
                    st.markdown(f"""
                    <div class="score-card">
                        <b>{name}</b><br>
                        <small>Status: {status}</small><br>
                        {score_summary}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No live cricket matches at the moment.")
except Exception as e:
    st.error(f"Error fetching live cricket scores: {e}")