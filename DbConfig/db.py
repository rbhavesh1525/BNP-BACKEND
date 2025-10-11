import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not ANON_KEY or not SERVICE_ROLE_KEY:
    raise ValueError("One or more Supabase environment variables are not set.")

# This is the primary, SAFE client for user authentication and public data access.
# It respects your Row-Level Security policies.
supabase_anon: Client = create_client(SUPABASE_URL, ANON_KEY)

# This is the ADMIN client. It bypasses all security policies.
# Use this ONLY for backend administrative tasks where you need to override security rules.
supabase_admin: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)