

import os
import pandas as pd
from app.services.features import extract_features
from app.services.model import train_model, load_model
from app.services.predictor import predict_with_confidence
from app.services.recommender import generate_recommendations

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/merged_data.xlsx")

def calculate_engagement_score(row):
    return (
        row.get("views", 0) * 0.2 +
        row.get("likes", 0) * 0.4 +
        row.get("comments", 0) * 0.4 +
        row.get("saves", 0) * 0.6 +
        row.get("clicks", 0) * 0.4
    )

def run_ab_testing():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found!")

    df = pd.read_excel(DATA_PATH).fillna(0)

    # Prepare features and target
    X, y = [], []
    for _, row in df.iterrows():
        X.append(extract_features(row))
        y.append(calculate_engagement_score(row))

    # Load or train model
    model = load_model()
    if model is None:
        print("Model not found or corrupt. Training new model...")
        model = train_model(X, y)

    results = []
    for _, row in df.iterrows():
        features = extract_features(row)
        a_score = calculate_engagement_score(row)
        b_score, confidence = predict_with_confidence(model, features)

        results.append({
            "content_preview": str(row.get("title", ""))[:60],
            "variant_a_score": round(a_score, 2),
            "variant_b_score": b_score,
            "confidence": confidence,
            "winner": "B" if b_score > a_score else "A",
            "recommendation": generate_recommendations(row)
        })

    return results
