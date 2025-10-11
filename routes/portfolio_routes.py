from fastapi import APIRouter, HTTPException
from schemas.portfolio import InvestmentRequest # Assuming this matches frontend
from Services.portfolio_service import generate_portfolio_service
from schemas.portfolio import RebalanceRequest, RebalanceResponse
from Services.portfolio_service import calculate_rebalancing_plan_service

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

        # Add these imports at the top of the file
from schemas.portfolio import RebalanceRequest, RebalanceResponse
from Services.portfolio_service import calculate_rebalancing_plan_service

# Add this new endpoint function to the file
@router.post("/rebalance_portfolio", response_model=RebalanceResponse)
async def rebalance_portfolio(data: RebalanceRequest):
    try:
        result = calculate_rebalancing_plan_service(data)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) # For bad input like invalid risk profile
    except Exception as e:
        # It's good practice to log the full error for debugging
        print(f"An error occurred during rebalancing: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred while calculating the rebalancing plan.")