def calculate_metrics(row):
    """
    Calculate performance metrics for a content item
    """

    views = row.get("views", 0)
    likes = row.get("likes", 0)
    comments = row.get("comments", 0)
    saves = row.get("saves", 0)
    clicks = row.get("clicks", 0)

    engagement_rate = 0
    if views > 0:
        engagement_rate = round((likes + comments + saves) / views, 3)

    click_through_rate = 0
    if views > 0:
        click_through_rate = round(clicks / views, 3)

    return {
        "views": int(views),
        "likes": int(likes),
        "comments": int(comments),
        "saves": int(saves),
        "clicks": int(clicks),
        "engagement_rate": engagement_rate,
        "click_through_rate": click_through_rate
    }
