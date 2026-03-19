import os
import sys
import traceback

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from sqlalchemy import Column, String
from app.db.base import Base
from app.db.session import SessionLocal

# Temporarily redefine User at runtime for testing
class TestUser(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String)

def diagnostic():
    db = SessionLocal()
    try:
        print("Testing Minimalist User Query...")
        u = db.query(TestUser).first()
        print(f"Success: {u.email}")
    except Exception:
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    diagnostic()
