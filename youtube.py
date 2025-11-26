from googleapiclient.discovery import build
import pandas as pd


# CONFIGURE YOUR API KEY

YOUTUBE_API_KEY = "AIzaSyCYiTiBazmkfYPUj8yTIvuzEcmj-yAMLV8"
CHANNEL_ID = "UCq-Fj5jknLsUf-MWSy4_brA"

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)



# GET VIDEO IDS

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



# GET VIDEO DETAILS

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


# Fetch data
video_ids = get_video_ids(CHANNEL_ID)
video_data = get_video_details(video_ids)

# Save to Excel
df = pd.DataFrame(video_data)
df.to_excel("youtube_data.xlsx", index=False)

print("YouTube data saved to youtube_data.xlsx")
