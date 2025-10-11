from fastapi import APIRouter, HTTPException
from schemas.authSchema import UserCreate, UserLogin
from Services.authSignup import create_new_user, login_user

# THIS LINE WAS MISSING
router = APIRouter()

@router.post("/signup")
async def signup(user_data: UserCreate):
    """
    API endpoint to handle user registration.
    """
    try:
        response = create_new_user(user_data)
        return response
    except HTTPException as e:
        raise e

@router.post("/login")
async def login(user_data: UserLogin):
    """
    API endpoint to handle user login.
    Returns the session data, including access and refresh tokens.
    """
    try:
        response = login_user(user_data)
        return response
    except HTTPException as e:
        raise e