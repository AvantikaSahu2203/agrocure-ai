import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.db.session import SessionLocal
from sqlalchemy import text
import traceback

def diagnostic():
    db = SessionLocal()
    try:
        print("Testing raw SQL SELECT * FROM users...")
        result = db.execute(text("SELECT * FROM users")).first()
        print(f"Raw SQL Result: {result}")
    except Exception:
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    diagnostic()
