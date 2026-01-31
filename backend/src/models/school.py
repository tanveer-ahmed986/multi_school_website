"""
School (tenant) model. Platform-wide table; no RLS.
"""
import uuid
from sqlalchemy import Column, String, Boolean, BigInteger, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from src.database.connection import Base


class School(Base):
    __tablename__ = "schools"

    school_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_name = Column(String(255), nullable=False)
    subdomain = Column(String(100), unique=True, nullable=False, index=True)
    logo_url = Column(Text, nullable=True)
    primary_color = Column(String(7), default="#0A3D62")
    secondary_color = Column(String(7), default="#EAF2F8")
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    config_json = Column(JSONB, nullable=False, server_default="{}")
    is_active = Column(Boolean, default=True, nullable=False)
    storage_used_bytes = Column(BigInteger, default=0, nullable=False)
    storage_limit_bytes = Column(BigInteger, default=10737418240, nullable=False)  # 10GB
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
