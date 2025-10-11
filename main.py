from fastapi import FastAPI
from DbConfig.db import supabase

# Import routers
from routes.mlresponse_route import router as ml_router
from routes import portfolio_routes, history_routes

# Initialize FastAPI
app = FastAPI(title="AI Portfolio Optimizer")

# Include routers
app.include_router(portfolio_routes.router, prefix="/api", tags=["Portfolio"])
app.include_router(history_routes.router, prefix="/api", tags=["History"])
app.include_router(ml_router, prefix="/api", tags=["ML Response"])

# Test Supabase
@app.get("/test-supabase")
def test_connection():
    try:
        _ = supabase.auth
        return {"status": "connected"}
    except Exception as e:
        return {"status": "not connected", "error": str(e)}

@app.get("/")
def root():
    return {"message": "Portfolio Prediction API is running 🚀"}
