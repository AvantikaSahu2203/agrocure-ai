import logging
import uuid
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.disease import DiseaseDetection
from app.models.user import User
from app.models.status_enums import DetectionStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CROPS = [
    {"name": "Tomato", "diseases": ["Early Blight", "Late Blight", "Healthy"]},
    {"name": "Potato", "diseases": ["Early Blight", "Late Blight", "Healthy"]},
    {"name": "Wheat", "diseases": ["Rust", "Mildew", "Healthy"]},
    {"name": "Rice", "diseases": ["Blast", "Brown Spot", "Healthy"]},
    {"name": "Grape", "diseases": ["Black Rot", "Esca", "Healthy"]}
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]

def seed_reports():
    db = SessionLocal()
    try:
        # Get target user
        user = db.query(User).filter(User.email == "farmer@agrocure.com").first()
        if not user:
            logger.error("User farmer@agrocure.com not found. Run seed_market_data.py first.")
            return

        logger.info(f"Seeding reports for user: {user.email}")

        # Clear existing detections for clean state (optional, but good for "real" feeling)
        # db.query(DiseaseDetection).filter(DiseaseDetection.user_id == user.id).delete()
        
        # Generate 50-100 random detections over the last 30 days
        num_detections = random.randint(50, 80)
        now = datetime.utcnow()

        for _ in range(num_detections):
            crop_info = random.choice(CROPS)
            disease = random.choice(crop_info["diseases"])
            severity = random.choice(SEVERITIES)
            if "Healthy" in disease:
                severity = "Low"
            
            # Random date in last 30 days
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            created_at = now - timedelta(days=days_ago, hours=hours_ago)

            detection = DiseaseDetection(
                id=str(uuid.uuid4()),
                user_id=user.id,
                image_url=f"https://picsum.photos/seed/{uuid.uuid4()}/400/300",
                detected_disease=disease,
                confidence_score=random.uniform(0.75, 0.99),
                status=DetectionStatus.COMPLETED,
                created_at=created_at,
                details={
                    "analysis": {
                        "disease": disease,
                        "severity": severity,
                        "crop_info": {
                            "name": crop_info["name"]
                        },
                        "recommendations": ["Use appropriate fungicide", "Monitor water levels"]
                    }
                }
            )
            db.add(detection)
        
        db.commit()
        logger.info(f"Successfully seeded {num_detections} report records.")

    except Exception as e:
        logger.error(f"Error seeding reports: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_reports()
