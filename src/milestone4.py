import pandas as pd
import os


def calculate_engagement_score(row):
    """
    Unified engagement score across platforms
    """

    views = row.get("views", 0)
    likes = row.get("likes", 0)
    yt_comments = row.get("comments", 0)

    upvotes = row.get("upvotes", 0)
    reddit_comments = row.get("reddit_comments", 0)

    saves = row.get("saves", 0)
    clicks = row.get("clicks", 0)

    score = (
        views * 0.2 +
        likes * 0.4 +
        yt_comments * 0.4 +
        upvotes * 0.5 +
        reddit_comments * 0.5 +
        saves * 0.6 +
        clicks * 0.4
    )

    return round(score, 2)


def run_milestone4():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(base_dir, "../data"))
    merged_file = os.path.join(data_dir, "merged_data.xlsx")

    df = pd.read_excel(merged_file)

    results = []

    for _, row in df.iterrows():
        content_text = str(
            row.get("title")
            or row.get("content")
            or row.get("description")
            or ""
        )

        # Variant A: Current performance
        variant_a_score = calculate_engagement_score(row)

        # Variant B: Predicted optimized performance (+20%)
        variant_b_score = round(variant_a_score * 1.20, 2)

        winner = "B" if variant_b_score > variant_a_score else "A"

        if winner == "B":
            recommendation = "Optimize headline, hashtags, and CTA"
        else:
            recommendation = "Current content strategy is effective"

        results.append({
            "content_preview": content_text[:60],
            "variant_a_score": variant_a_score,
            "variant_b_score": variant_b_score,
            "winner": winner,
            "recommendation": recommendation
        })

    output_df = pd.DataFrame(results)
    output_file = os.path.join(data_dir, "ab_testing_results.xlsx")
    output_df.to_excel(output_file, index=False)

    return {
        "processed_records": len(results),
        "output_file": "ab_testing_results.xlsx",
        "message": "A/B testing and prediction completed successfully"
    }
