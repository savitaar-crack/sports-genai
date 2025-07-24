import feedparser

def fetch_espn_news(limit=5):
    url = "https://www.espn.com/espn/rss/news"
    feed = feedparser.parse(url)
    headlines = []

    for entry in feed.entries[:limit]:
        headlines.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link
        })
    
    return headlines
# Script to scrape or fetch sports news
