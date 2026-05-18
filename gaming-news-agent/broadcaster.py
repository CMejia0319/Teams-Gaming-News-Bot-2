import requests
import json
from config import TEAMS_WEBHOOK_URL

def broadcast_to_teams(message):
    """
    Sends the curated message to a Microsoft Teams channel via webhook.
    """
    if not TEAMS_WEBHOOK_URL or TEAMS_WEBHOOK_URL == "your_teams_webhook_url_here":
        print("ERROR: Teams Webhook URL is missing or invalid.")
        return False
        
    if not message or message == "No new gaming news at this time.":
        print("No significant news to broadcast.")
        return True

    headers = {
        "Content-Type": "application/json"
    }
    
    # Simple markdown message payload for Teams
    # Teams webhooks support a basic structure, Adaptive Cards are better but text is simpler and reliable
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "🎮 **Gaming News Update** 🎮",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }

    try:
        response = requests.post(
            TEAMS_WEBHOOK_URL, 
            headers=headers, 
            data=json.dumps(payload)
        )
        
        if response.status_code == 200 or response.status_code == 202:
            print("Successfully broadcasted to Teams!")
            return True
        else:
            print(f"Failed to broadcast to Teams. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error broadcasting to Teams: {e}")
        return False
