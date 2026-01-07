import os
import pickle
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

def train_model(X, y):
    """Train a RandomForestRegressor and save it."""
    model = RandomForestRegressor()
    model.fit(X, y)

    # Save the model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"Model trained and saved to {MODEL_PATH}")
    return model

def load_model():
    """Load the model if it exists. Return None if missing or corrupted."""
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            print("Warning: Model file corrupted. Will retrain.")
            return None
    return None
