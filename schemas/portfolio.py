from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RebalancePreferences(BaseModel):
    frequency_years: int
    equity_decrease_percent: float

class InvestmentRequest(BaseModel):
    investment_amount: float = Field(..., alias="amount")
    risk_profile: str = Field(..., alias="risk")
    tenure: int
    selected_assets: Optional[List[str]] = None
    investment_type: Optional[str] = None
    return_expectation: Optional[float] = None
    rebalance_preferences: Optional[RebalancePreferences] = None

class AssetProjection(BaseModel):
    predicted_return: float
    raw_model_prediction: float
    weight: float

class FeatureContribution(BaseModel):
    feature: str
    feature_value: float
    contribution: float

class AssetExplanation(BaseModel):
    top_feature_contributions: List[FeatureContribution]
    intercept: float

class PortfolioSummary(BaseModel):
    expected_return: float
    expected_value: float
    risk_level: str
    top_assets_driving_returns: List[str]

class PortfolioResponse(BaseModel):
    input_summary: Dict[str, Any]
    portfolio_allocation: Dict[str, float]
    per_asset_projection: Dict[str, AssetProjection]
    per_asset_explanations: Optional[Dict[str, AssetExplanation]] = None
    portfolio_summary: PortfolioSummary
# Add these new classes to the file

class CurrentHolding(BaseModel):
    asset_name: str = Field(..., description="The name of the asset, e.g., 'S&P 500 (includes dividends)'")
    current_value: float = Field(..., gt=0, description="The current market value of this holding")

class RebalanceRequest(BaseModel):
    current_holdings: List[CurrentHolding]
    risk_profile: str = Field(..., description="The target risk profile, e.g., 'low', 'moderate', 'high'")

class RebalanceAction(BaseModel):
    asset_name: str
    action: str # "Sell" or "Buy"
    amount: float = Field(..., description="The dollar amount to buy or sell")

class RebalanceResponse(BaseModel):
    target_allocation: Dict[str, float]
    rebalancing_actions: List[RebalanceAction]
    total_portfolio_value: float