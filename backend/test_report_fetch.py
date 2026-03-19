import requests

def test_fetch_report():
    # Attempt to fetch as farmer@agrocure.com
    # First, get a token (assuming we know the password or can bypass)
    # Since I'm on the server, I'll just check the DB directly to see who owns which report.
    pass

if __name__ == "__main__":
    from app.db.session import SessionLocal
    from app.models.disease import DiseaseDetection
    from app.models.user import User
    
    db = SessionLocal()
    latest = db.query(DiseaseDetection).order_by(DiseaseDetection.created_at.desc()).first()
    if latest:
        user = db.query(User).filter(User.id == latest.user_id).first()
        print(f"Report ID: {latest.id}")
        print(f"Owner: {user.email if user else 'None'}")
        print(f"Details exists: {latest.details is not None}")
    else:
        print("No reports found.")
    db.close()
