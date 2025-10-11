import os
import pickle
import json
import pandas as pd
from Models.prediction_logic import predict_portfolio
from schemas.portfolio import InvestmentRequest
from Models.prediction_logic import risk_allocation # Import the risk dictionary
from schemas.portfolio import RebalanceRequest, RebalanceAction # Import new schemas



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
    # Add this new function to the service file
from Models.prediction_logic import risk_allocation # Import the risk dictionary
from schemas.portfolio import RebalanceRequest, RebalanceAction # Import new schemas

def calculate_rebalancing_plan_service(data: RebalanceRequest):
    """
    Calculates the buy/sell actions needed to align a user's current portfolio
    with their target risk profile allocation.
    """
    # 1. Calculate total portfolio value and current allocation weights
    total_value = sum(holding.current_value for holding in data.current_holdings)
    
    current_allocation = {
        holding.asset_name: holding.current_value / total_value 
        for holding in data.current_holdings
    }

    # 2. Get the target allocation for the desired risk profile
    try:
        target_allocation = risk_allocation[data.risk_profile.lower()]
    except KeyError:
        raise ValueError(f"Invalid risk profile '{data.risk_profile}'. Must be one of {list(risk_allocation.keys())}")

    # 3. Determine the difference and calculate buy/sell actions
    rebalancing_actions = []
    
    # Use all asset names from both current and target to ensure none are missed
    all_asset_names = set(current_allocation.keys()) | set(target_allocation.keys())

    for asset in all_asset_names:
        current_value = current_allocation.get(asset, 0) * total_value
        target_value = target_allocation.get(asset, 0) * total_value
        
        difference = target_value - current_value
        
        if abs(difference) > 0.01: # Only suggest trades for meaningful amounts
            action = "Buy" if difference > 0 else "Sell"
            rebalancing_actions.append(
                RebalanceAction(
                    asset_name=asset,
                    action=action,
                    amount=round(abs(difference), 2)
                )
            )

    return {
        "total_portfolio_value": round(total_value, 2),
        "target_allocation": target_allocation,
        "rebalancing_actions": rebalancing_actions
    }