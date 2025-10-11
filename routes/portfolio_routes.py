from fastapi import APIRouter, HTTPException
from schemas.portfolio import InvestmentRequest # Assuming this matches frontend
from Services.portfolio_service import generate_portfolio_service

router = APIRouter()

@router.post("/generate_portfolio")
async def generate_portfolio(data: InvestmentRequest):
    try:
        # The service now returns the exact JSON structure needed by the frontend
        result = generate_portfolio_service(data)
        return result
    except Exception as e:
        # It's good practice to log the full error for debugging
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred while generating the portfolio.")