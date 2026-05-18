import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
TIMEZONE = os.getenv("TIMEZONE", "America/Los_Angeles")

# RSS Feeds for gaming news
RSS_FEEDS = {
    "IGN": "http://feeds.ign.com/ign/news",
    "Polygon": "https://www.polygon.com/rss/index.xml",
    "Kotaku": "https://kotaku.com/rss",
    "GameSpot": "https://www.gamespot.com/feeds/news/"
}

if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    print("WARNING: OPENAI_API_KEY is not set or is using the default template value.")
    
if not TEAMS_WEBHOOK_URL or TEAMS_WEBHOOK_URL == "your_teams_webhook_url_here":
    print("WARNING: TEAMS_WEBHOOK_URL is not set or is using the default template value.")
