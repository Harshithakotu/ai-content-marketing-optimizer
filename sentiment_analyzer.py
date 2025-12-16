import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def analyze_sentiment(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Classify sentiment as Positive, Negative, or Neutral. Return ONLY the label."
                },
                {"role": "user", "content": text}
            ]
        )

        sentiment_label = response.choices[0].message.content.strip()

        if sentiment_label.lower() == "positive":
            score = 1
        elif sentiment_label.lower() == "negative":
            score = -1
        else:
            score = 0

        return {
            "sentiment": sentiment_label,
            "score": score
        }

    except Exception as e:
        print("Groq Error:", e)
        return {"sentiment": "Neutral", "score": 0}
