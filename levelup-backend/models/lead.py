from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.sql import func
from core.database import Base
import enum

class LeadStatus(str, enum.Enum):
    new      = "new"
    contacted = "contacted"
    qualified = "qualified"
    converted = "converted"
    lost      = "lost"

class Lead(Base):
    __tablename__ = "leads"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(150), index=True, nullable=False)
    phone      = Column(String(20), nullable=True)
    company    = Column(String(150), nullable=True)
    message    = Column(Text, nullable=True)
    source     = Column(String(60), default="website")   # website / referral / ad
    status     = Column(Enum(LeadStatus), default=LeadStatus.new)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
