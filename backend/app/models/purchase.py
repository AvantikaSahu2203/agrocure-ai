from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    store_id = Column(String, ForeignKey("stores.id"), nullable=False)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="purchases")
    store = relationship("Store", backref="sales")
    medicine = relationship("Medicine")
