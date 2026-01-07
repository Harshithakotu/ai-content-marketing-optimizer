from fastapi import FastAPI
from milestone4 import run_milestone4

app = FastAPI(
    title="AI Marketing A/B Testing & Prediction Coach",
    description="Data-driven A/B testing using YouTube, Reddit, and Pinterest metrics",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "A/B Testing API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "A/B Testing & Prediction Coach",
        "deployment": "active"
    }


@app.post("/run-ab-test")
def run_ab_testing():
    return run_milestone4()
