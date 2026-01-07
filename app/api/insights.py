from fastapi import APIRouter
import pandas as pd
from app.services.sentiment import analyze_sentiment
from app.services.performance import calculate_metrics  # returns number

router = APIRouter(prefix="/insights", tags=["Insights"])

@router.get("/")
def get_insights():
    df = pd.read_excel("data/merged_data.xlsx").fillna(0)

    total_contents = len(df)
    sentiments = []
    engagement_scores = []

    top_content_list = []
    low_content_list = []

    for _, row in df.iterrows():
        text = str(row.get("title", "") or row.get("content", ""))
        sentiment_score = analyze_sentiment(text)  # float
        sentiments.append(sentiment_score)

        engagement_score = calculate_metrics(row)  # int or float
        engagement_scores.append(engagement_score)

        preview = text[:60]
        content_entry = {
            "content_preview": preview,
            "sentiment_score": sentiment_score,
            "engagement_score": engagement_score,
            "sentiment": "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
        }

        top_content_list.append(content_entry)
        low_content_list.append(content_entry)

    # Sort top/low
    top_content_list = sorted(top_content_list, key=lambda x: x["engagement_score"], reverse=True)[:10]
    low_content_list = sorted(low_content_list, key=lambda x: x["engagement_score"])[:10]

    response = {
        "status": "success",
        "insights": {
            "total_contents": total_contents,
            "average_sentiment": round(sum(sentiments)/len(sentiments), 2) if sentiments else 0,
            "average_engagement": round(sum(engagement_scores)/len(engagement_scores), 2) if engagement_scores else 0,
            "sentiment_distribution": {
                "Positive": sum(1 for s in sentiments if s > 0),
                "Neutral": sum(1 for s in sentiments if s == 0),
                "Negative": sum(1 for s in sentiments if s < 0),
            },
            "top_performing_content": top_content_list,
            "low_performing_content": low_content_list
        }
    }

    return response
