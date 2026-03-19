from typing import Optional
from datetime import date
from pydantic import BaseModel
from uuid import UUID

from app.models.status_enums import CropStatus

# Shared properties
class CropBase(BaseModel):
    name: Optional[str] = None
    planting_date: Optional[date] = None
    status: Optional[CropStatus] = CropStatus.HEALTHY
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    expected_harvest_date: Optional[date] = None
    variety: Optional[str] = None
    area_size: Optional[float] = None
    area_unit: Optional[str] = "Acres"
    location_name: Optional[str] = None
    image_url: Optional[str] = None

# Properties to receive on crop creation
class CropCreate(CropBase):
    name: str
    variety: Optional[str] = None
    expected_harvest_date: Optional[date] = None
    area_size: Optional[float] = None
    area_unit: Optional[str] = "Acres"
    location_name: Optional[str] = None
    image_url: Optional[str] = None

# Properties to receive on crop update
class CropUpdate(CropBase):
    pass

# Properties shared by models stored in DB
class CropInDBBase(CropBase):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True

# Properties to return to client
class Crop(CropInDBBase):
    pass

# Properties stored in DB
class CropInDB(CropInDBBase):
    pass
