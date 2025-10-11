import os
import pickle
import json
import pandas as pd
from Models.prediction_logic import predict_portfolio
from schemas.portfolio import InvestmentRequest


# --- 1. LOAD ALL MODEL ARTIFACTS ONCE AT STARTUP ---
try:
    # THIS IS THE SECTION THAT WAS FIXED
    # Build a robust path starting from the project's root directory.
    # Assumes the developer runs the server from the 'BNP-BACKEND' folder.
    PROJECT_ROOT_DIR = os.getcwd() 
    MODELS_DIR = os.path.join(PROJECT_ROOT_DIR, "Models")
    
    MODELS_PATH = os.path.join(MODELS_DIR, "linear_asset_models.pkl")
    FEATURES_PATH = os.path.join(MODELS_DIR, "linear_feature_columns.pkl")
    LATEST_DATA_PATH = os.path.join(MODELS_DIR, "latest_features.json")

    with open(MODELS_PATH, "rb") as f:
        all_models = pickle.load(f)

    with open(FEATURES_PATH, "rb") as f:
        feature_cols = pickle.load(f)

    with open(LATEST_DATA_PATH, "r") as f:
        latest_features = json.load(f)
        
except FileNotFoundError as e:
    # This error message now gives a clearer instruction
    raise RuntimeError(f"A model file was not found. Ensure you are running the server from the 'BNP-BACKEND' root directory. Path check failed for: {e}")


# --- 2. DEFINE THE SERVICE FUNCTION ---
def generate_portfolio_service(data: InvestmentRequest):
    """
    This service function acts as a bridge. It takes the frontend request,
    formats it for the ML function, and returns the complete result.
    """
    # Convert the Pydantic model into a simple dictionary for your function
    user_input = {
        "amount": data.investment_amount,
        "risk_profile": data.risk_profile,
        "tenure": data.tenure,
        "return_expectation": data.return_expectation,
        "rebalance_preferences": data.rebalance_preferences.dict() if data.rebalance_preferences else {}
    }
    
    # Call your complete prediction function with all necessary components
    prediction_result = predict_portfolio(
        user_input=user_input,
        models=all_models,
        feature_cols_dict=feature_cols,
        latest_features_data=latest_features
    )
    
    # The result from your function is already a complete JSON-ready dictionary.
    # We can return it directly.
    return prediction_result