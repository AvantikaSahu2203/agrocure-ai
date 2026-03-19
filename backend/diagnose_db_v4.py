import os
import sys
import traceback

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

try:
    from app.db.session import SessionLocal
    from app.models.user import User
    from sqlalchemy import select
    
    print("Initializing session...")
    db = SessionLocal()
    try:
        print("Testing SQLAlchemy 2.0 select...")
        stmt = select(User).where(User.email == "farmer@agrocure.com")
        print(f"Statement created: {stmt}")
        result = db.execute(stmt).scalar_one_or_none()
        print(f"Result: {result.email if result else 'Not found'}")
        
    except Exception:
        print("--- ERROR DURING EXECUTION ---")
        traceback.print_exc()
    finally:
        db.close()
        print("Session closed.")
except Exception:
    print("--- ERROR DURING INITIALIZATION ---")
    traceback.print_exc()
