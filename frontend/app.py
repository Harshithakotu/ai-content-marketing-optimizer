import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# =============================
# Page setup
# =============================
st.set_page_config(page_title="AI Marketing Dashboard", layout="wide")
st.title("🚀 AI Marketing Intelligence Dashboard")

# =============================
# Backend endpoints
# =============================
# Backend URLs
API_BASE = "http://127.0.0.1:8000"
ENDPOINTS = {
    "Dashboard": f"{API_BASE}/dashboard/stats",
    "Insights": f"{API_BASE}/insights/",
    "Optimization": f"{API_BASE}/optimize/",
    "AB Testing": f"{API_BASE}/ab-testing/run"
}

# =============================
# Sidebar menu
# =============================
menu = ["Dashboard", "Insights", "Optimization", "AB Testing"]
choice = st.sidebar.selectbox("Select View", menu)

# =============================
# Helper to call backend
# =============================
def get_api_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error ({response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return None

# =============================
# Helper: Compute engagement score if not in backend
# =============================
def compute_engagement_score(df):
    df["engagement_score"] = (
        df.get("views", 0) * 0.2 +
        df.get("likes", 0) * 0.4 +
        df.get("comments", 0) * 0.4 +
        df.get("saves", 0) * 0.6 +
        df.get("clicks", 0) * 0.4
    )
    return df

def fetch(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

# =============================
# Dashboard Tab
# =============================
if choice == "Dashboard":
    st.header("📊 Dashboard Overview")
    data = get_api_data(ENDPOINTS["Dashboard"])
    if data:
        df = pd.DataFrame(data.get("stats", []))
        if df.empty:
            st.info("No dashboard data available.")
        else:
            # Metrics cards
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Contents", df["total_contents"].sum() if "total_contents" in df else 0)
            col2.metric("Avg Engagement", round(df["avg_engagement"].mean(), 2) if "avg_engagement" in df else 0)
            col3.metric("Top Performing Content", df["top_content"].iloc[0] if "top_content" in df else "-")

            # Bar chart of top 10 content by engagement
            if "engagement_score" in df.columns:
                top_df = df.sort_values("engagement_score", ascending=False).head(10)
                st.subheader("Top 10 Contents by Engagement")
                st.bar_chart(top_df.set_index("content_preview")["engagement_score"],width='stretch')

# =============================
# Insights Tab
# =============================
elif choice == "Insights":
    st.header("🔍 Content Insights")

    data = fetch(f"{API_BASE}/insights/")
    if not data or data.get("status") != "success":
        st.info("No insights available")
    else:
        insights = data["insights"]

        # =============================
        # Top Metrics
        # =============================
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Contents", insights.get("total_contents", 0))
        col2.metric("Avg Sentiment", insights.get("average_sentiment", 0))
        col3.metric("Avg Engagement", insights.get("average_engagement", 0))

        st.divider()

        # =============================
        # Sentiment Distribution
        # =============================
        st.subheader("📊 Sentiment Distribution")

        sentiment_dist = insights.get("sentiment_distribution", {})
        if sentiment_dist:
            sentiment_df = pd.DataFrame(
                sentiment_dist.items(),
                columns=["Sentiment", "Count"]
            ).set_index("Sentiment")

            st.bar_chart(sentiment_df)
        else:
            st.info("No sentiment distribution data available.")

        st.divider()

        # =============================
        # Top Performing Content
        # =============================
        st.subheader("🔥 Top Performing Content")

        top_content = insights.get("top_performing_content", [])
        if top_content:
            top_df = pd.DataFrame(top_content)
            st.dataframe(
                top_df[[
                    "content_preview",
                    "sentiment",
                    "sentiment_score",
                    "engagement_score"
                ]],
                use_container_width='stretch'
            )
        else:
            st.info("No top performing content found.")

        st.divider()

        # =============================
        # Low Performing Content
        # =============================
        st.subheader("⚠️ Content Needing Optimization")

        low_content = insights.get("low_performing_content", [])
        if low_content:
            low_df = pd.DataFrame(low_content)
            st.dataframe(
                low_df[[
                    "content_preview",
                    "sentiment",
                    "sentiment_score",
                    "engagement_score"
                ]],
                use_container_width='stretch'
            )
        else:
            st.info("No low performing content found.")

        st.success("✅ Insights loaded successfully")




# =============================
# Optimization Tab
# =============================
elif choice == "Optimization":
    st.header("⚡ Optimization Recommendations")

    # Input box for the content to optimize
    text_to_optimize = st.text_area("Paste content to optimize here:")

    if st.button("Optimize Content") and text_to_optimize:
        try:
            response = requests.post(
                ENDPOINTS["Optimization"],  # http://127.0.0.1:8000/optimize/
                json={"text": text_to_optimize}  # send text as query param
            )
            if response.status_code == 200:
                data = response.json()
                st.subheader("Original Content")
                st.write(data.get("original", ""))

                st.subheader("Optimized Content")
                st.write(data.get("optimized", ""))
            else:
                st.error(f"API Error {response.status_code}")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
    elif not text_to_optimize:
        st.info("Please paste some content above to get optimization recommendations.")


# =============================
# AB Testing Tab
# =============================
elif choice == "AB Testing":
    st.header("🧪 AB Testing Results")
    if st.button("Run AB Testing"):
        with st.spinner("Running AB Testing..."):
            data = get_api_data(ENDPOINTS["AB Testing"])
            if data:
                df = pd.DataFrame(data.get("results", []))
                if df.empty:
                    st.info("No AB testing results yet.")
                else:
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Contents", len(df))
                    col2.metric("Avg Confidence", round(df["confidence"].mean(), 2))
                    col3.metric("Variant B Wins", (df["winner"] == "B").sum())

                    # Insights per content
                    st.subheader("📊 AB Testing Insights")
                    for _, row in df.iterrows():
                        st.markdown(f"""
### {row['content_preview']}
- 🅰 Current Score: {row['variant_a_score']}
- 🅱 Predicted Score: {row['variant_b_score']}
- 🎯 Confidence: {row['confidence']}
- 🏆 Winner: Variant {row['winner']}
- 💡 Recommendation: **{row['recommendation']}**
""")
