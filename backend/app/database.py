from supabase import create_client, Client
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_anon_key)

def get_supabase_client() -> Client:
    """Get the Supabase client instance."""
    return supabase

def get_service_client() -> Client:
    """Get the Supabase service client for admin operations."""
    return create_client(settings.supabase_url, settings.supabase_service_key)

async def test_connection():
    """Test the database connection."""
    try:
        # Try to query the profiles table
        response = supabase.table('profiles').select('id').limit(1).execute()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
