import os
import sys
import traceback

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

try:
    from app.db.session import SessionLocal
    from app.models.user import User
    from sqlalchemy import text
    
    print("Initializing session...")
    db = SessionLocal()
    try:
        print("Testing raw SQL...")
        result = db.execute(text("SELECT 1")).scalar()
        print(f"Raw SQL result: {result}")
        
        print("Testing ORM query...")
        user = db.query(User).filter(User.email == "farmer@agrocure.com").first()
        print(f"ORM Result: {user.email if user else 'Not found'}")
        
    except Exception:
        print("--- ERROR DURING EXECUTION ---")
        traceback.print_exc()
    finally:
        db.close()
        print("Session closed.")
except Exception:
    print("--- ERROR DURING INITIALIZATION ---")
    traceback.print_exc()
