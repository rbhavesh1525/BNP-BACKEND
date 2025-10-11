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
