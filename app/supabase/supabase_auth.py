import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def signup_user(email: str, password: str):
    return supabase.auth.sign_up({"email": email, "password": password})

def login_user(email: str, password: str):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})
