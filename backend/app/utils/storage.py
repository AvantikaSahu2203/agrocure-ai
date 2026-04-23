import uuid
from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

supabase: Client = None

if settings.SUPABASE_URL and settings.SUPABASE_KEY:
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        logger.info("Supabase client initialized for storage.")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")

async def upload_image_to_cloud(image_bytes: bytes, filename: str = None) -> str:
    """
    Uploads an image to Supabase Storage and returns the public URL.
    Falls back to local path string if cloud is not configured.
    """
    if not filename:
        filename = f"{uuid.uuid4()}.jpg"

    if supabase:
        try:
            bucket = settings.SUPABASE_BUCKET
            path = f"diagnosis/{filename}"
            
            # Upload to Supabase
            res = supabase.storage.from_(bucket).upload(
                path=path,
                file=image_bytes,
                file_options={"content-type": "image/jpeg"}
            )
            
            # Get Public URL
            url = supabase.storage.from_(bucket).get_public_url(path)
            logger.info(f"Image uploaded to cloud: {url}")
            return url
        except Exception as e:
            logger.error(f"Cloud upload failed: {e}")
            # Fallback to local-style naming for the DB record
            return f"uploads/{filename}"
    
    # Fallback to local naming if no cloud config
    return f"uploads/{filename}"
