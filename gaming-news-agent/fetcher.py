import feedparser
import time
import os
import json
from config import RSS_FEEDS

SEEN_ARTICLES_FILE = "seen_articles.json"

def load_seen_articles():
    if os.path.exists(SEEN_ARTICLES_FILE):
        try:
            with open(SEEN_ARTICLES_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_seen_articles(seen):
    with open(SEEN_ARTICLES_FILE, "w", encoding="utf-8") as f:
        # Limit to the last 1000 items to avoid infinite growth
        json.dump(list(seen)[-1000:], f)

def fetch_latest_news():
    """
    Fetches the latest unseen articles from all configured RSS feeds.
    Returns a list of dictionaries with 'title', 'link', 'summary', and 'source'.
    """
    seen_articles = load_seen_articles()
    new_articles = []
    
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                link = entry.get('link')
                if link and link not in seen_articles:
                    # Filter out entries that might be too old, but for simplicity we rely on 'seen' list.
                    # In a production app, we might also check published date.
                    title = entry.get('title', 'No Title')
                    # Get summary or fallback to description
                    summary = entry.get('summary', entry.get('description', ''))
                    
                    new_articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'source': source
                    })
                    seen_articles.add(link)
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
            
    save_seen_articles(seen_articles)
    return new_articles
