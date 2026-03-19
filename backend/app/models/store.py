from sqlalchemy import Column, String, ForeignKey, Float, JSON, Boolean
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Inventory relationship
    # inventory = Column(JSON, nullable=True) # Deprecated in favor of StoreInventory table 

    owner = relationship("User", backref="stores")
