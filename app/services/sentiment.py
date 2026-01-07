def analyze_sentiment(text: str) -> float:
    if not text.strip():
        return 0.0

    # TEMP SIMPLE LOGIC (replace later with ML)
    positive_words = ["good", "great", "love", "excellent", "best"]
    negative_words = ["bad", "worst", "poor", "hate"]

    score = 0
    for word in positive_words:
        if word in text.lower():
            score += 1
    for word in negative_words:
        if word in text.lower():
            score -= 1

    return round(score / 5, 2)
