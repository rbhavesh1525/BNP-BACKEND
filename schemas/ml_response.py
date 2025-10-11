from pydantic import BaseModel
from typing import Optional, Dict, Any

class MLResponseSchema(BaseModel):
    user_id: Optional[int]
    invested_amount: Optional[int]
    tenure_years: Optional[int]
    risk_level: Optional[str]
    allocation: Optional[Dict[str, Any]]
    investment_type: Optional[str]
    asset_returns: Optional[Dict[str, Any]]
    yearly_values: Optional[Dict[str, Any]]
    projected_final_value: Optional[int]
    projected_cagr: Optional[float]
    recommendation: Optional[Dict[str, Any]]
    is_saved: Optional[bool] = True
