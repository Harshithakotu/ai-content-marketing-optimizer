import pandas as pd
import os
import time

from analysis.sentiment_analyzer import analyze_sentiment
from analysis.performance_metrics import simulate_performance_metrics
from analysis.slack_notifier import send_slack_alert


def main():
    print("Loading merged data...")

    base_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(base_dir, "../data"))
    merged_file = os.path.join(data_dir, "merged_data.xlsx")

    df = pd.read_excel(merged_file)

    print("Running sentiment analysis + performance metrics...")

    sentiments = []
    scores = []
    reach_list = []
    engagement_list = []
    virality_list = []

    for idx, row in df.iterrows():

        text = str(
            row.get("title")
            or row.get("content")
            or row.get("description")
            or ""
        )

        sentiment = analyze_sentiment(text)
        metrics = simulate_performance_metrics(text)

        sentiments.append(sentiment["sentiment"])
        scores.append(sentiment["score"])
        reach_list.append(metrics["estimated_reach"])
        engagement_list.append(metrics["engagement_rate"])
        virality_list.append(metrics["virality_score"])

        #  INTELLIGENT ALERT LOGIC
        alert_messages = []

        if sentiment["score"] == -1:
            alert_messages.append(
                f"🚨 Negative Sentiment Detected\n"
                f"Source: {row.get('source', 'Unknown')}\n"
                f"Sentiment: {sentiment['sentiment']}\n"
                f"Action: Review content immediately."
            )

        if metrics["virality_score"] >= 0.8:
            alert_messages.append(
                f"🔥 High Viral Potential\n"
                f"Source: {row.get('source', 'Unknown')}\n"
                f"Virality Score: {metrics['virality_score']}\n"
                f"Action: Promote this content."
            )

        if metrics["engagement_rate"] <= 1:
            alert_messages.append(
                f"📉 Low Engagement Alert\n"
                f"Source: {row.get('source', 'Unknown')}\n"
                f"Engagement Rate: {metrics['engagement_rate']}\n"
                f"Action: Improve headline or CTA."
            )

        # Send alerts ONLY if needed
        for msg in alert_messages:
            send_slack_alert(msg)
            time.sleep(1)  # Slack safety

    # Save results
    df["sentiment"] = sentiments
    df["sentiment_score"] = scores
    df["estimated_reach"] = reach_list
    df["engagement_rate"] = engagement_list
    df["virality_score"] = virality_list

    output_file = os.path.join(data_dir, "analysis_results.xlsx")
    df.to_excel(output_file, index=False)

    send_slack_alert(
        f"Processed {len(df)} records.\n"
        f"Alerts generated based on sentiment & performance."
    )

    print(f"Analysis complete! Saved")


if __name__ == "__main__":
    main()
