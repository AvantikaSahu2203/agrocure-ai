from datetime import timedelta
from typing import Any, Optional
import json
import traceback

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.firebase_auth import verify_firebase_token
import random
import string

router = APIRouter()

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Standard OAuth2 compatible token login.
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/json")
def login_json(
    data: Any = Body(...)
) -> Any:
    """
    Super-Nuclear Path - No dependencies, no schemas, no serialization.
    """
    from app.db.session import SessionLocal
    import traceback
    
    db = None
    try:
        # 1. Force a clean session
        db = SessionLocal()
        
        # 2. Extract data (Permissive)
        username = None
        password = None
        
        if isinstance(data, dict):
            username = data.get("username")
            password = data.get("password")
        elif isinstance(data, str):
            try:
                data_dict = json.loads(data)
                username = data_dict.get("username")
                password = data_dict.get("password")
            except:
                pass
        
        if not username: username = getattr(data, "username", None)
        if not password: password = getattr(data, "password", None)

        print(f"DEBUG: Login Request received for: '{username}'")
        
        if not username or not password:
            return {"detail": "Missing credentials"}, 400

        # 3. Manual Authentication
        user = crud.user.authenticate(db, email=username, password=password)
        
        if not user:
            print(f"DEBUG: Auth failed for '{username}'")
            return {"detail": "Incorrect email or password"}, 400
        
        # 4. Create Token manually
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
        
        # 5. Return RAW dict
        return {
            "access_token": token,
            "token_type": "bearer",
        }
        
    except Exception as e:
        print(f"SUPER-NUCLEAR CRASH:")
        traceback.print_exc()
        return {"detail": f"Server Crash: {str(e)}"}, 500
    finally:
        if db:
            db.close()

@router.post("/login/phone", response_model=schemas.Token)
def login_phone(
    db: Session = Depends(deps.get_db),
    firebase_token: str = Body(..., embed=True)
) -> Any:
    """
    Login or Register via Firebase Phone OTP Token
    """
    # 1. Verify Firebase Token
    decoded_token = verify_firebase_token(firebase_token)
    phone_number = decoded_token.get("phone_number")
    
    if not phone_number:
        raise HTTPException(
            status_code=400, 
            detail="Token does not contain a verified phone number"
        )

    # 2. Get or Create User
    user = crud.user.get_by_phone(db, phone_number=phone_number)
    if not user:
        # Create a new user account automatically for new verified phones
        # Using phone number as a temporary email/username if needed
        user_in = schemas.UserCreate(
            email=f"phone_{phone_number}@agrocure.ai",
            password=security.get_password_hash(phone_number), # Dummy password
            phone_number=phone_number,
            full_name=decoded_token.get("name", "Farmer")
        )
        user = crud.user.create(db, obj_in=user_in)

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # 3. Issue Backend JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/signup")
def signup(
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate = Body(...)
) -> Any:
    """
    Register a new user, auto-verify, and return access token (OTP Bypassed).
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists in the system.",
        )
    
    # 1. Create User as already verified
    user_in.is_verified = True
    user = crud.user.create(db, obj_in=user_in)
    
    # 2. Generate token immediately
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    # 3. Return both user and token
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login/verify", response_model=schemas.Token)
def verify_email(
    db: Session = Depends(deps.get_db),
    email: str = Body(...),
    code: str = Body(...)
) -> Any:
    """
    Verify email with code and return token.
    """
    email = email.strip()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Magic bypass for even faster dev
    if code == "123456" or user.verification_code == code:
        crud.user.update(db, db_obj=user, obj_in={"is_verified": True, "verification_code": None})
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
            "user": user
        }
    
    raise HTTPException(status_code=400, detail="Invalid verification code")
