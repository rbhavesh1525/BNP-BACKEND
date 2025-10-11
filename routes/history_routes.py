from fastapi import APIRouter
from Services.history_service import fetch_portfolio_by_id, fetch_all_portfolios

router = APIRouter()

@router.get("/portfolio/{portfolio_id}")
async def get_portfolio(portfolio_id: str):
    return await fetch_portfolio_by_id(portfolio_id)

@router.get("/portfolios")
async def get_all_portfolios():
    return await fetch_all_portfolios()
