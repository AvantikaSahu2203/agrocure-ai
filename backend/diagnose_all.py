import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.crop import Crop
import traceback

def diagnostic():
    db = SessionLocal()
    try:
        print("--- Testing User Model ---")
        try:
            u = db.query(User).first()
            print(f"User Query Success: {u}")
        except Exception:
            print("User Query FAILED")
            traceback.print_exc()
            
        print("\n--- Testing Crop Model ---")
        try:
            c = db.query(Crop).first()
            print(f"Crop Query Success: {c}")
        except Exception:
            print("Crop Query FAILED")
            traceback.print_exc()
            
    finally:
        db.close()

if __name__ == "__main__":
    diagnostic()
