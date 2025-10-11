import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/linear_asset_models.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "../models/linear_feature_columns.pkl")

# --- Load model safely ---
with open(MODEL_PATH, "rb") as f:
    loaded_obj = pickle.load(f)

if isinstance(loaded_obj, dict):
    if "model" in loaded_obj:
        model = loaded_obj["model"]
    else:
        model = next((v for v in loaded_obj.values() if hasattr(v, "predict")), None)
        if model is None:
            raise ValueError("No valid model found in pickle file.")
else:
    model = loaded_obj

# --- Load feature columns ---
with open(FEATURES_PATH, "rb") as f:
    feature_columns = pickle.load(f)

if isinstance(feature_columns, dict):
    feature_columns = list(feature_columns.keys())

def predict_portfolio(data: dict):
    """
    Predicts portfolio returns using the pre-trained linear model.
    Fills missing features and reorders columns.
    """
    try:
        df = pd.DataFrame([data])

        # Add missing columns with default 0
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0

        # Reorder columns
        df = df[feature_columns]

        prediction = model.predict(df)

        return {
            "input": data,
            "prediction": float(prediction[0]),
            "status": "success"
        }

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {e}")
