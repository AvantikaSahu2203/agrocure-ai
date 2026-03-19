from sqlalchemy import Column, Float, ForeignKey, DateTime, Boolean, String
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base

class WeatherLog(Base):
    __tablename__ = "weather_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    crop_id = Column(String, ForeignKey("crops.id"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rain_forecast = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    crop = relationship("Crop", backref="weather_logs")
