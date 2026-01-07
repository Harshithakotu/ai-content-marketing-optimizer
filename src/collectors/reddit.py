
import requests
import pandas as pd

SUBREDDIT = "marketing"
LIMIT = 50

def fetch_posts(subreddit, limit=50):
    url = f"https://api.pullpush.io/reddit/search/submission/?subreddit={subreddit}&size={limit}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error:", response.status_code)
        return []

    data = response.json().get("data", [])
    posts = []

    for post in data:
        posts.append({
            "title": post.get("title"),
            "author": post.get("author"),
            "score": post.get("score"),
            "num_comments": post.get("num_comments"),
            "url": post.get("full_link"),
            "text": post.get("selftext"),
        })

    return posts


print("Fetching Reddit posts...")
posts = fetch_posts(SUBREDDIT, LIMIT)

df = pd.DataFrame(posts)
filename = "../../data/reddit_data.xlsx"
df.to_excel(filename, index=False)

print("Done! Check reddit_data.xlsx")
