from DbConfig.db import supabase_anon
from fastapi import HTTPException

async def fetch_portfolio_by_id(portfolio_id: str):
    response = supabase.table("portfolios").select("*").eq("id", portfolio_id).execute()
    
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return response.data[0]

async def fetch_all_portfolios():
    response = supabase.table("portfolios").select("*").execute()
    
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    
    return response.data
