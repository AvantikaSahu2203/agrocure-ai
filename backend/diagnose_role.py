import os
import sys
import traceback
import enum

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from sqlalchemy import Column, String, Enum
from app.db.base import Base
from app.db.session import SessionLocal
from app.models.status_enums import UserRole

# Redefine User at runtime for testing
class TestUser(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String)
    role = Column(Enum(UserRole))

def diagnostic():
    db = SessionLocal()
    try:
        print("Testing User Model with Role field...")
        u = db.query(TestUser).first()
        print(f"Success: {u.email} - Role: {u.role}")
    except Exception:
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    diagnostic()
