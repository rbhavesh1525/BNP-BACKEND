from fastapi import APIRouter
from pydantic import BaseModel
from services.gemini_service import extract_keywords
from models.recommendation_model import build_recommendation

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/investment-recommendation")
async def investment_recommendation(request: PromptRequest):
    prompt = request.prompt
    
    # 1️⃣ Extract keywords via Gemini
    keywords = extract_keywords(prompt)
    
    # 2️⃣ Generate recommendation
    recommendation = build_recommendation(keywords)
    
    # 3️⃣ Return combined response
    return {
        "prompt": prompt,
        "keywords": keywords,
        "recommendation": recommendation
    }
