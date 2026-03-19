from sqlalchemy import Column, String, Enum, Text
# from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    manufacturer = Column(String, nullable=True)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
