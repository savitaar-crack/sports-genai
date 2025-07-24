# 🏟️ Sports GenAI

**Sports GenAI** is a generative AI-powered sports assistant that provides real-time news, player bios, and intelligent insights — using the power of the **Groq API (LLaMA 3)** and sports data APIs.

---

## 🚀 Features

- 🧠 **AI-Powered Player Biographies** – Generates summaries using LLaMA 3 via Groq API.
- 📰 **Live Sports News** – Fetches top headlines from ESPN.
- 👤 **Player Info Search** – Search players by full name using TheSportsDB.
- 🧹 **Modular Design** – Clean file structure with separation of concerns.
- ✅ **Ready for Deployment** – Easily deploy on Render, Railway, or Hugging Face.

---

## 📁 Project Structure

```
sports-genai/
├── app/
│   ├── main.py           # Streamlit app
│   ├── config.py
│   └── rag_engine.py     # For future RAG extensions
├── scripts/
│   ├── groq_response.py  # AI bio generation
│   ├── ingest_news.py    # ESPN RSS parsing
│   ├── sportsdb_api.py   # Player search API
│   └── ...               # Other utility scripts
├── .env.example          # Sample environment setup
├── .gitignore
├── README.md
├── requirements.txt
└── venv/ (excluded)
```

---

## ⚙️ Setup Instructions

### 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### 🧪 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### ▶️ Run the App

```bash
streamlit run app/main.py
```

---

## 🌐 APIs Used

- 🧠 **[Groq API](https://console.groq.com/)** – LLaMA 3 inference for generating bios.
- 📰 **[ESPN RSS Feed](https://www.espn.com/espn/rss/news)** – Latest sports news.
- 📊 **[TheSportsDB](https://www.thesportsdb.com/)** – Player stats and photos.

---

## 📸 Screenshots

> *(You can add images later by uploading to `/assets/` folder and embedding here)*

---

## 📄 License

MIT License © 2025 Savitaar

---

## 💡 Future Roadmap

- Add vector search & embeddings (RAG)
- Deploy to Hugging Face Spaces
- Add sport-specific stats (e.g. cricket, football, F1)
