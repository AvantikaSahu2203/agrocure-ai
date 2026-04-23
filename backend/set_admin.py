import argparse
import sys
import os

# Add current dir to path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.user import User
from app.models.status_enums import UserRole

def set_admin(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"❌ User with email {email} not found.")
            return
        
        user.role = UserRole.ADMIN
        db.commit()
        print(f"✅ User {email} is now an ADMIN! Relog in the app to see admin features.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set a user as Admin")
    parser.add_argument("--email", required=True, help="User email")
    args = parser.parse_args()
    set_admin(args.email)
