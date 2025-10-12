import pandas as pd
import numpy as np
import json

# -----------------------------
# 1️⃣ Load Historical Data
# -----------------------------
def load_historical_data():
    """
    Simulated historical returns for assets.
    Replace with real 50-year dataset in production.
    """
    data = {
        'Year': range(2015, 2025),
        'Gold': [0.12, 0.08, 0.05, 0.18, 0.10, 0.02, 0.15, 0.08, -0.05, 0.07],
        'Bond': [0.06, 0.05, 0.04, 0.07, 0.06, 0.03, 0.05, 0.06, 0.02, 0.04],
        'RealEstate': [0.10, 0.12, 0.08, 0.15, 0.11, 0.09, 0.13, 0.12, 0.05, 0.08],
        'Stock': [0.18, 0.20, 0.15, 0.25, 0.22, 0.10, 0.18, 0.21, -0.10, 0.12],
        'Crypto': [0.35, 0.40, 0.30, 0.50, 0.42, 0.25, 0.38, 0.45, -0.15, 0.28]
    }
    return pd.DataFrame(data)

historical_data = load_historical_data()

# -----------------------------
# 2️⃣ Keyword Extraction
# -----------------------------
keywords_map = {
    'risk': ['low', 'medium', 'moderate', 'high'],
    'return': ['safe', 'decent', 'medium', 'high', 'aggressive'],
    'tenure': ['short', 'medium', 'long', 'years', 'year', 'month', 'months', '1','2','3','4','5','10']
}

def extract_keywords(prompt, keywords_map):
    prompt_lower = prompt.lower()
    extracted = {}
    for key, words in keywords_map.items():
        for word in words:
            if word in prompt_lower:
                # Special handling for tenure numbers
                if key == 'tenure' and word.isdigit():
                    extracted[key] = int(word)
                else:
                    extracted[key] = word
                break
    return extracted

# -----------------------------
# 3️⃣ Risk Profile to Allocation
# -----------------------------
def get_portfolio_allocation(risk_profile):
    risk_profile = risk_profile.lower()
    if risk_profile == 'high':
        return {'Gold': 0.1, 'Bond': 0.15, 'RealEstate': 0.15, 'Stock': 0.4, 'Crypto': 0.2}
    elif risk_profile in ['medium', 'moderate']:
        return {'Gold': 0.15, 'Bond': 0.25, 'RealEstate': 0.15, 'Stock': 0.3, 'Crypto': 0.15}
    else:  # Low risk
        return {'Gold': 0.25, 'Bond': 0.3, 'RealEstate': 0.2, 'Stock': 0.15, 'Crypto': 0.1}

# -----------------------------
# 4️⃣ Predict Expected Growth
# -----------------------------
def predict_future_growth(df):
    predictions = {}
    for col in df.columns[1:]:
        mean_return = df[col].mean()
        # Add small random variation to simulate prediction
        predicted = mean_return + np.random.uniform(-0.02, 0.02)
        predictions[col] = round(predicted, 3)
    return predictions

predicted_growth = predict_future_growth(historical_data)

# -----------------------------
# 5️⃣ Select Best Asset
# -----------------------------
def get_best_asset(assets, risk_profile):
    risk_map = {
        'low': ['Low'],
        'medium': ['Low','Medium'],
        'moderate': ['Low','Medium'],
        'high': ['Low','Medium','High']
    }
    allowed_risks = risk_map.get(risk_profile.lower(), ['Low'])
    
    filtered = [a for a in assets if a['risk'] in allowed_risks and a['expected_growth'] > 0]
    if not filtered:
        filtered = assets
    
    # Sort by expected growth first, then avg return
    sorted_assets = sorted(filtered, key=lambda x: (x['expected_growth'], x['avg_return']), reverse=True)
    return sorted_assets[0]

# -----------------------------
# 6️⃣ Build Recommendation JSON
# -----------------------------
def build_recommendation(prompt):
    keywords = extract_keywords(prompt, keywords_map)
    risk = keywords.get('risk', 'low')
    allocation = get_portfolio_allocation(risk)
    
    suitable_assets = []
    for asset, weight in allocation.items():
        if weight > 0:
            avg_return = historical_data[asset].mean()
            expected_growth = predicted_growth.get(asset, 0)
            suitable_assets.append({
                'name': asset,
                'avg_return': round(avg_return, 2),
                'risk_profile': 'Low' if asset in ['Gold','Bond'] else 'Medium' if asset=='RealEstate' else 'High',
                'expected_growth': expected_growth
            })
    
    # Rank assets by expected growth
    suitable_assets_sorted = sorted(suitable_assets, key=lambda x: x['expected_growth'], reverse=True)
    recommended = get_best_asset(suitable_assets_sorted, risk)
    
    output = {
        'prompt': prompt,
        'extracted_keywords': keywords,
        'portfolio_allocation': allocation,
        'all_assets': suitable_assets_sorted,
        'recommended_asset': recommended,
        'portfolio_expected_growth': round(sum([a['expected_growth']*allocation[a['name']] for a in suitable_assets_sorted]), 3)
    }
    
    return output

# -----------------------------
# 7️⃣ Main Execution
# -----------------------------
if __name__ == "__main__":
    user_prompt = input("Enter your investment goal or preference: ")
    recommendation = build_recommendation(user_prompt)
    
    # Pretty-print JSON output
    print("\nStructured Recommendation Output:\n")
    print(json.dumps(recommendation, indent=2))
