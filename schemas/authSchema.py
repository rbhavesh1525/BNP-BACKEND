from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: str
    full_name: Optional[str] = None
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str