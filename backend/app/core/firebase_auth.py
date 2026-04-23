import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status
from app.core.config import settings

# Path to the service account key
# The user should place their serviceAccountKey.json in app/core/
CERT_PATH = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

def init_firebase():
    """
    Initialize Firebase Admin SDK for Production.
    """
    if not firebase_admin._apps:
        cert_path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
        if os.path.exists(cert_path):
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred)
            print(f"INFO: Firebase Admin SDK initialized for project: {settings.FIREBASE_PROJECT_ID}")
        else:
            # Fallback for local development if creds aren't there yet
            # CRITICAL: Token verification WILL fail without valid serviceAccountKey.json
            firebase_admin.initialize_app()
            print("WARNING: Firebase Admin initialized WITHOUT service account. PROD AUTH WILL FAIL.")

def verify_firebase_token(id_token: str):
    """
    Verifies a Firebase ID token.
    Returns the decoded token (including uid and phone_number).
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Firebase token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Run initialization on module load
init_firebase()
