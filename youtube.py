
from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

# ---------------------------
# Explicitly load .env file (Option B for OneDrive)
# ---------------------------
env_path = Path(r"C:\Users\kotuh\OneDrive\Documents\Desktop\AI-Marketing-Data-collector\p.env")
load_dotenv(dotenv_path=env_path)

# ---------------------------
# Get API key and Channel ID
# ---------------------------
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# ---------------------------
# Debug checks
# ---------------------------
print("API Key Loaded Successfully")
print("Channel ID Loaded Successfully")

# ---------------------------
# Initialize YouTube API client
# ---------------------------
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# ---------------------------
# Get video IDs from the channel
# ---------------------------
def get_video_ids(channel_id):
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )
    response = request.execute()

    video_ids = [
        item["id"]["videoId"]
        for item in response["items"]
        if item["id"]["kind"] == "youtube#video"
    ]
    return video_ids

# ---------------------------
# Get video details
# ---------------------------
def get_video_details(video_ids):
    data_list = []

    for vid in video_ids:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=vid
        )
        response = request.execute()

        for item in response["items"]:
            data = {
                "video_id": vid,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "publishedAt": item["snippet"]["publishedAt"],
                "views": item["statistics"].get("viewCount", 0),
                "likes": item["statistics"].get("likeCount", 0),
                "comments": item["statistics"].get("commentCount", 0),
            }
            data_list.append(data)

    return data_list

# ---------------------------
# Run the script
# ---------------------------
video_ids = get_video_ids(CHANNEL_ID)
if not video_ids:
    print("No videos found for this channel.")
else:
    video_data = get_video_details(video_ids)

    # Save to Excel
    df = pd.DataFrame(video_data)
    df.to_excel("youtube_data.xlsx", index=False)

    print("YouTube data saved to youtube_data.xlsx")
