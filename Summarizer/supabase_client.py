from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = "https://egyfupjorjczjfkmnusd.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Or replace with hardcoded key (not recommended)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)