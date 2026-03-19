from sqlalchemy import Column, Integer, ForeignKey, Float, String
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class StoreInventory(Base):
    __tablename__ = "store_inventory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    store_id = Column(String, ForeignKey("stores.id"), nullable=False)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, nullable=False)

    store = relationship("Store", backref="inventory_items")
    medicine = relationship("Medicine")
