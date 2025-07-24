import sys
import os
# Add to your imports at the top
from scripts.live_scores import get_live_football_scores, get_live_cricket_scores
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from scripts.ingest_news import fetch_espn_news
from scripts.sportsdb_api import search_player
from scripts.groq_response import generate_summary_from_gpt  # Now uses Groq

# Load environment variables
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Sports GenAI", layout="wide")
st.title("🏟️ Sports GenAI Chat")

# --- Section 1: Groq Q&A
st.markdown("### 🤖 Ask Anything About Sports")
general_question = st.text_input("Ask me anything about sports (e.g., 'Who won the FIFA World Cup in 2018?')")

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


# --- Section 2: Player Lookup
st.markdown("### 🔎 Search a Player")
player_name = st.text_input("Enter a player’s full name:")

if player_name:
    st.write(f"Searching info for: {player_name}")
    player = search_player(player_name)

    if player:
        name = player.get("strPlayer", "Unknown")
        position = player.get("strPosition", "N/A")
        nationality = player.get("strNationality", "N/A")
        st.success(f"**{name}** ({position} - {nationality})")

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

# --- Section 3: News Feed
st.markdown("---")
st.subheader("🗞️ Top Sports Headlines (Live from ESPN)")

news_items = fetch_espn_news(limit=5)
for item in news_items:
    st.markdown(f"### [{item['title']}]({item['link']})")
    st.caption(item['summary'])

# --- Section 4: Live Scores
st.markdown("---")
st.subheader("🏏⚽ Live Scores")

with st.expander("⚽ Live Football Matches"):
    football_matches = get_live_football_scores()
    if football_matches:
        for match in football_matches[:5]:
            home = match["homeTeam"]
            away = match["awayTeam"]
            full_time = match["score"]["fullTime"]
            st.markdown(
                f"**{home} {full_time.get('home', 0)} - {full_time.get('away', 0)} {away}**"
            )
    else:
        st.info("No live football matches at the moment or failed to fetch.")

with st.expander("🏏 Live Cricket Matches"):
    cricket_matches = get_live_cricket_scores()
    if cricket_matches:
        for match in cricket_matches[:5]:
            name = match.get("name", "Match")
            status = match.get("status", "Unknown")
            score = match.get("score", [])
            score_summary = " | ".join([
                f"{s.get('inning', '')}: {s.get('runs', '')}/{s.get('wickets', '')}" for s in score
            ]) if score else "No score yet"
            st.markdown(f"**{name}** - {status} - *{score_summary}*")
    else:
        st.info("No live cricket matches at the moment.")
