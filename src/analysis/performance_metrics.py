import random


def simulate_performance_metrics(content_text: str) -> dict:
    
   # Mock performance metrics
    

    return {
        "estimated_reach": random.randint(500, 5000),
        "engagement_rate": round(random.uniform(0.5, 8.0), 2),
        "virality_score": round(random.uniform(0.1, 1.0), 2)
    }
