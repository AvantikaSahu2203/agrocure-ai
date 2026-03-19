from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from app.models.status_enums import DetectionStatus

# Shared properties
class DiseaseDetectionBase(BaseModel):
    image_url: Optional[str] = None
    detected_disease: Optional[str] = None
    confidence_score: Optional[float] = None
    details: Optional[Any] = None
    status: Optional[DetectionStatus] = DetectionStatus.PENDING

# Properties to receive on creation
class DiseaseDetectionCreate(DiseaseDetectionBase):
    image_url: str
    crop_id: Optional[UUID] = None

# Properties to receive on update
class DiseaseDetectionUpdate(DiseaseDetectionBase):
    pass

# Properties shared by models stored in DB
class DiseaseDetectionInDBBase(DiseaseDetectionBase):
    id: UUID
    user_id: UUID
    crop_id: Optional[UUID] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Properties to return to client
class DiseaseDetection(DiseaseDetectionInDBBase):
    pass

# Alias for compatibility
DiseaseDetectionInDB = DiseaseDetectionInDBBase
