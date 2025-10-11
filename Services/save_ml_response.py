from DbConfig.db import supabase_admin

def save_model_response(data: dict):
    response = supabase.table("Model-response").insert(data).execute()
    return response
