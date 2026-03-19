import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.db.session import SessionLocal
from app import crud, schemas

def test_db_logic():
    print("Testing DB connection...")
    db = SessionLocal()
    try:
        print("Fetching user by email...")
        user = crud.user.get_by_email(db, email="farmer@agrocure.com")
        print(f"Found user: {user.email if user else 'Not found'}")
        
        # Test auth logic
        if user:
            print("Testing authentication...")
            auth_user = crud.user.authenticate(db, email="farmer@agrocure.com", password="password")
            print(f"Auth result: {'Success' if auth_user else 'Failed'}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_db_logic()
