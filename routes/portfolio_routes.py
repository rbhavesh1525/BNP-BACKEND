from fastapi import APIRouter, HTTPException
from schemas.portfolio import InvestmentRequest
from Services.portfolio_service import generate_portfolio_service

router = APIRouter()

@router.post("/generate_portfolio")
async def generate_portfolio(data: InvestmentRequest):
    try:
        result = generate_portfolio_service(data)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
