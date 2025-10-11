import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import json

# ==============================================================================
# SECTION 1: PREDICTION LOGIC
# This part stays outside the gatekeeper.
# The server needs to import this function and dictionary.
# ==============================================================================

risk_allocation = {
    "low": {
        "S&P 500 (includes dividends)": 0.15,
        "US Small cap (bottom decile)": 0.05,
        "3-month T.Bill": 0.25,
        "US T. Bond (10-year)": 0.25,
        "Baa Corporate Bond": 0.15,
        "Real Estate": 0.10,
        "Gold*": 0.05
    },
    "moderate": {
        "S&P 500 (includes dividends)": 0.30,
        "US Small cap (bottom decile)": 0.10,
        "3-month T.Bill": 0.10,
        "US T. Bond (10-year)": 0.15,
        "Baa Corporate Bond": 0.10,
        "Real Estate": 0.15,
        "Gold*": 0.10
    },
    "high": {
        "S&P 500 (includes dividends)": 0.40,
        "US Small cap (bottom decile)": 0.20,
        "3-month T.Bill": 0.05,
        "US T. Bond (10-year)": 0.10,
        "Baa Corporate Bond": 0.05,
        "Real Estate": 0.10,
        "Gold*": 0.10
    }
}

def predict_portfolio(user_input: dict, models: dict, feature_cols_dict: dict, latest_features_data: dict):
    amount = user_input.get("amount", 100000)
    tenure = user_input.get("tenure", 5)
    risk_profile = user_input.get("risk_profile", "moderate")
    rebalancing_prefs = user_input.get("rebalance_preferences", {})

    allocation = risk_allocation[risk_profile.lower()]

    per_asset = {}
    per_asset_explanations = {}
    portfolio_expected_return = 0.0

    latest_features = pd.Series(latest_features_data)

    for asset, weight in allocation.items():
        features = feature_cols_dict[asset]
        X_latest = latest_features[features].values.reshape(1, -1)
        pred = models[asset].predict(X_latest)[0]

        pred_adj = pred * (1 + 0.02 * (tenure - 1))

        portfolio_expected_return += pred_adj * weight

        contributions = []
        coefs = models[asset].coef_
        for f, coef in zip(features, coefs):
            contributions.append({
                "feature": f,
                "feature_value": float(latest_features[f]),
                "contribution": float(latest_features[f] * coef)
            })

        per_asset[asset] = {
            "predicted_return": float(pred_adj),
            "raw_model_prediction": float(pred),
            "weight": weight
        }
        per_asset_explanations[asset] = {
            "top_feature_contributions": sorted(contributions, key=lambda x: abs(x["contribution"]), reverse=True)[:3],
            "intercept": float(models[asset].intercept_)
        }

    portfolio_value = amount * (1 + portfolio_expected_return)

    rebalancing_plan = []
    if rebalancing_prefs:
        freq = rebalancing_prefs.get("frequency_years", 2)
        eq_decrease = rebalancing_prefs.get("equity_decrease_percent", 5)
        years = int(tenure // freq)
        temp_allocation = allocation.copy()
        for i in range(1, years + 1):
            for eq_asset in ["S&P 500 (includes dividends)", "US Small cap (bottom decile)"]:
                temp_allocation[eq_asset] = max(temp_allocation[eq_asset] - eq_decrease/100, 0)
            rebalancing_plan.append({
                "year": i*freq,
                "action": f"Reduce equity weight by {eq_decrease}%",
                "new_allocation": temp_allocation.copy()
            })

    guidance = [
        f"Expected portfolio return: {portfolio_expected_return:.3f}",
        "Equity assets contribute most to returns for moderate/high risk profiles.",
        "Bonds and T-Bills stabilize portfolio in low/moderate risk profiles."
    ]

    output_json = {
        "input_summary": user_input,
        "portfolio_allocation": allocation,
        "per_asset_projection": per_asset,
        "per_asset_explanations": per_asset_explanations,
        "portfolio_summary": {
            "expected_portfolio_return": portfolio_expected_return,
            "expected_portfolio_value": portfolio_value,
            "top_drivers": sorted(allocation.keys(), key=lambda x: per_asset[x]['predicted_return']*allocation[x], reverse=True)[:3],
            "risk_level": risk_profile
        },
        "rebalancing_plan": rebalancing_plan,
        "user_guidance": guidance
    }

    return output_json


# ==============================================================================
# SECTION 2: TRAINING LOGIC
# This part is now inside the if _name_ == "_main_": block.
# It will ONLY run if you execute this script directly (e.g., python prediction_logic.py).
# The server will IGNORE this block when it imports the file.
# ==============================================================================

if __name__ == "__main__":
    
    # --- Step 1: Load & preprocess dataset ---
    print("Running training script...")
    file_path = "histretSP45783b8.xls" # Assumes the XLS is in the same folder when running
    df = pd.read_excel(file_path, sheet_name="Returns by year", header=19)
    df = df.dropna(axis=1, how='all')
    df.columns = [col.strip() if isinstance(col, str) else f"Col_{i}" for i, col in enumerate(df.columns)]

    asset_cols = [
        "S&P 500 (includes dividends)", "US Small cap (bottom decile)", "3-month T.Bill",
        "US T. Bond (10-year)", "Baa Corporate Bond", "Real Estate", "Gold*"
    ]
    macro_cols = ["Inflation Rate", "Historical ERP"]

    for col in asset_cols + macro_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=asset_cols + macro_cols).reset_index(drop=True)

    for col in asset_cols + macro_cols:
        for lag in range(1, 4):
            df[f'{col}_lag{lag}'] = df[col].shift(lag)
    for col in asset_cols:
        df[f'{col}_roll_mean'] = df[col].rolling(window=3).mean()
        df[f'{col}_roll_std'] = df[col].rolling(window=3).std()
        df[f'{col}_momentum'] = df[f'{col}_lag1'] - df[f'{col}_lag2']

    df['Inflation_ERP_interaction'] = df['Inflation Rate'] * df['Historical ERP']
    df = df.dropna().reset_index(drop=True)

    # --- Step 2: Train linear regression models ---
    models = {}
    feature_cols_dict = {}

    for col in asset_cols:
        features = (
            [f'{col}_lag{i}' for i in range(1, 4)] +
            [f'{m}_lag{i}' for m in macro_cols for i in range(1, 4)] +
            [f'{col}_roll_mean', f'{col}_roll_std', f'{col}_momentum'] +
            ['Inflation_ERP_interaction']
        )
        X = df[features].astype(float)
        y = df[col].astype(float)
        model = LinearRegression()
        model.fit(X, y)
        models[col] = model
        feature_cols_dict[col] = features
    
    # --- Step 3: Save artifacts for backend ---
    with open("linear_asset_models.pkl", "wb") as f:
        pickle.dump(models, f)

    with open("linear_feature_columns.pkl", "wb") as f:
        pickle.dump(feature_cols_dict, f)

    latest_features_dict = df.iloc[-1].to_dict()
    with open("latest_features.json", "w") as f:
        json.dump(latest_features_dict, f)

    print("✅ Models, feature columns, and latest features saved successfully!")