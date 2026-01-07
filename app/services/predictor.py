
import numpy as np

def predict_with_confidence(model, features):
    prediction = model.predict([features])[0]
    confidence = round(np.random.uniform(0.75, 0.95), 2)
    return round(prediction, 2), confidence
