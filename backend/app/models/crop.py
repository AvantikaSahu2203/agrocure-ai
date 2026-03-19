from sqlalchemy import Column, String, ForeignKey, Date, Enum, Float
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base
import enum

from app.models.status_enums import CropStatus

class Crop(Base):
    __tablename__ = "crops"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    planting_date = Column(Date, nullable=True)
    expected_harvest_date = Column(Date, nullable=True)
    variety = Column(String, nullable=True)
    area_size = Column(Float, nullable=True)
    area_unit = Column(String, default="Acres")
    location_name = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    
    status = Column(Enum(CropStatus), default=CropStatus.HEALTHY)
    
    # Location specific to this crop
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user = relationship("User", backref="crops")
