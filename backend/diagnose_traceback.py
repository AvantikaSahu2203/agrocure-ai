import os
import sys
import traceback

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.db.session import SessionLocal
from app.models.user import User

def diagnostic():
    db = SessionLocal()
    try:
        print("Executing db.query(User).first()...")
        u = db.query(User).first()
        print(f"Success: {u}")
    except Exception:
        with open("full_traceback.txt", "w") as f:
            traceback.print_exc(file=f)
        print("FAILED. Traceback written to full_traceback.txt")
    finally:
        db.close()

if __name__ == "__main__":
    diagnostic()
