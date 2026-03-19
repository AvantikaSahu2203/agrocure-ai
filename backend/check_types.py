import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app.models.user import User
print(f"User type: {type(User)}")
print(f"User is instance: {isinstance(User, type)}")

from app.db.base import Base
print(f"Base type: {type(Base)}")

from app.db.session import SessionLocal
db = SessionLocal()
print(f"Session type: {type(db)}")
db.close()
