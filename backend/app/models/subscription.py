from sqlalchemy import Column, Enum, DateTime, Boolean, ForeignKey, String
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base
import enum

class PlanType(str, enum.Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan_type = Column(Enum(PlanType), default=PlanType.FREE)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", backref="subscription")
