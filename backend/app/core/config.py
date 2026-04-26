import os

class Settings:
    PROJECT_NAME: str = "AgroCure AI"
    
    # Base directory for local SQLite fallback
    _BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _DEFAULT_DB_PATH = os.path.join(_BASE_DIR, "sql_app.db").replace("\\", "/")
    
    # Database Configuration (Auto-handles Postgres naming mismatches in Cloud)
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    DATABASE_URL: str = db_url or f"sqlite:///{_DEFAULT_DB_PATH}"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "7b9e8c1d2e3f4a5b6c7d8e9f0a1b2c3d") 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    
    # External APIs
    FIREBASE_SERVICE_ACCOUNT_PATH: str = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "app/core/serviceAccountKey.json")
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "agrocure-ai")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Supabase Storage Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_BUCKET: str = os.getenv("SUPABASE_BUCKET", "diagnosis")

settings = Settings()
