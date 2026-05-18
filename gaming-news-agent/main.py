import schedule
import time
from datetime import datetime
import pytz
from config import TIMEZONE
from fetcher import fetch_latest_news
from summarizer import get_summaries
from broadcaster import broadcast_to_teams

def job(is_morning_update=False):
    print(f"\n--- Running Gaming News Job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    # 1. Fetch news
    print("Fetching latest news...")
    articles = fetch_latest_news()
    
    if not articles:
        print("No new articles found. Skipping broadcast.")
        return
        
    print(f"Found {len(articles)} new articles.")
    
    # 2. Summarize using OpenAI
    print("Summarizing with OpenAI...")
    time_context = "the last 24 hours" if is_morning_update else "the last 2 hours"
    summary = get_summaries(articles, time_context=time_context)
    
    # 3. Broadcast to Teams
    print("Broadcasting to Teams...")
    success = broadcast_to_teams(summary)
    if success:
        print("Job completed successfully.")
    else:
        print("Job finished with broadcast errors.")

def run_scheduler():
    print(f"Starting Autonomous Gaming News Agent...")
    print(f"Timezone configured as: {TIMEZONE}")
    
    # Get local timezone dynamically or use configured
    tz = pytz.timezone(TIMEZONE)
    
    # Schedule the 9 AM "Big News" blast
    # `schedule` uses local time. If server is in UTC, we might need to adjust, 
    # but let's assume it runs on a machine where local time matches desired time.
    # To ensure exact timezone matching, we can do manual check in a while loop, 
    # or just rely on server time if it's the user's local PC.
    # Since the prompt says "9 AM", we use the server's local time.
    
    schedule.every().day.at("09:00").do(job, is_morning_update=True)
    
    # Schedule the bi-hourly updates
    schedule.every().day.at("11:00").do(job, is_morning_update=False)
    schedule.every().day.at("13:00").do(job, is_morning_update=False)
    schedule.every().day.at("15:00").do(job, is_morning_update=False)
    schedule.every().day.at("17:00").do(job, is_morning_update=False)
    
    print("Scheduler initialized.")
    print("Jobs scheduled for: 09:00, 11:00, 13:00, 15:00, 17:00 local time.")
    
    # Run once immediately on startup for testing purposes (Optional)
    # print("Running initial startup check...")
    # job(is_morning_update=False)
    
    while True:
        schedule.run_pending()
        time.sleep(60) # Wait a minute before checking schedule again

if __name__ == "__main__":
    run_scheduler()
