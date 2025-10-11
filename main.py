from fastapi import FastAPI
from DbConfig.db import supabase

app = FastAPI()

@app.get("/test-supabase")
def test_connection():
    try:
        _ = supabase.auth  
        return {"status": "connected"}
    except Exception as e:
        return {"status": "not connected", "error": str(e)}
