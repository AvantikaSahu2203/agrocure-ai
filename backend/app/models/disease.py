from sqlalchemy import Column, String, ForeignKey, Float, DateTime, Enum, JSON
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base
import enum

from app.models.status_enums import DetectionStatus

class DiseaseDetection(Base):
    __tablename__ = "disease_detections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    crop_id = Column(String, ForeignKey("crops.id"), nullable=True) # Can be null if checking without saving crop
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    image_url = Column(String, nullable=False)
    detected_disease = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    details = Column(JSON, nullable=True) # Full AI output
    status = Column(Enum(DetectionStatus), default=DetectionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="detections")
    crop = relationship("Crop", backref="detections")
