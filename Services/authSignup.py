# Import the SAFE anonymous client
from DbConfig.db import supabase_anon
from schemas.authSchema import UserCreate, UserLogin
from fastapi import HTTPException

def create_new_user(user_data: UserCreate):
    """
    Signs up a new user using the safe, anonymous Supabase client.
    """
    try:
        sign_up_options = {
            "data": {
                "username": user_data.username,
                "full_name": user_data.full_name
            }
        }
        
        # Use the safe anon client for signup
        user = supabase_anon.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": sign_up_options,
        })
        
        if user.user:
            return {"message": "User created successfully. Please check your email to verify."}
        if user.error:
            raise HTTPException(status_code=400, detail=str(user.error.message))
        raise HTTPException(status_code=500, detail="An unknown error occurred during signup.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def login_user(user_data: UserLogin):
    """
    Logs in a user using the safe, anonymous Supabase client.
    """
    try:
        # Use the safe anon client for login
        session = supabase_anon.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })

        if session.session:
            return session
        if session.error:
            raise HTTPException(status_code=401, detail=str(session.error.message))
        raise HTTPException(status_code=500, detail="An unknown error occurred during login.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")