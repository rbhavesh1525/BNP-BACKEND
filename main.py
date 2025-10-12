from fastapi import FastAPI
# CORRECTED: Import supabase_anon, not supabase
from DbConfig.db import supabase_anon 

from fastapi.middleware.cors import CORSMiddleware
# Import routers
from routes.mlresponse_route import router as ml_router
# CORRECTED: Import the new auth router
from routes import portfolio_routes, history_routes, authRoutes

# Initialize FastAPI
app = FastAPI(title="AI Portfolio Optimizer")

# Include routers
app.include_router(portfolio_routes.router, prefix="/api", tags=["Portfolio"])
app.include_router(history_routes.router, prefix="/api", tags=["History"])
app.include_router(ml_router, prefix="/api", tags=["ML Response"])
# CORRECTED: Include the auth router to make /signup and /login work
app.include_router(authRoutes.router, prefix="/api/auth", tags=["Authentication"])

origins = [
    "http://localhost:5173",  # your frontend URL
    "http://127.0.0.1:8000",  # in case Vite uses 127.0.0.1
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not recommended in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test Supabase
@app.get("/test-supabase")
def test_connection():
    try:
        # CORRECTED: Use supabase_anon, which is the imported client
        _ = supabase_anon.auth.get_user()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "not connected", "error": str(e)}

@app.get("/")
def root():
    return {"message": "Portfolio Prediction API is running 🚀"}