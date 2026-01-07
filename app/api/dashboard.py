from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../data/merged_data.xlsx"
)

@router.get("/stats")
def dashboard_stats():
    try:
        if not os.path.exists(DATA_PATH):
            return {"stats": []}

        df = pd.read_excel(DATA_PATH).fillna(0)

        if df.empty:
            return {"stats": []}

        # SAFELY get columns (no KeyError)
        views = df.get("views", 0)
        likes = df.get("likes", 0)
        comments = df.get("comments", 0)
        saves = df.get("saves", 0)
        clicks = df.get("clicks", 0)

        engagement = (
            views * 0.2 +
            likes * 0.4 +
            comments * 0.4 +
            saves * 0.6 +
            clicks * 0.4
        )

        top_title = "N/A"
        if "title" in df.columns:
            top_title = str(df.iloc[0]["title"])[:60]

        return {
            "stats": [
                {
                    "total_contents": len(df),
                    "avg_engagement": round(float(engagement.mean()), 2),
                    "top_content": top_title
                }
            ]
        }

    except Exception as e:
        # NEVER crash the API
        return {
            "stats": [],
            "error": str(e)
        }
