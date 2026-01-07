from slack_sdk import WebClient  
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

client = WebClient(token=SLACK_TOKEN) if SLACK_TOKEN else None


def send_slack_alert(message: str):
    if not client:
        print("[Slack Disabled] Message:", message)
        return

    try:
        client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        print("[Slack] Alert sent!")
    except SlackApiError as e:
        print("Slack Error:", e.response["error"])
