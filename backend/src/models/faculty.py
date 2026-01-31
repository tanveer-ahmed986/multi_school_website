"""
Faculty member model. Tenant-scoped by school_id.
"""
import uuid
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.connection import Base


class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.school_id", ondelete="CASCADE"), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    designation = Column(String(100), nullable=False)
    qualification = Column(String(255), nullable=False)
    experience_years = Column(Integer, nullable=False)  # CHECK >= 0 in migration
    subject = Column(String(100), nullable=True)
    photo_url = Column(Text, nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    school = relationship("School", backref="faculty", foreign_keys=[school_id])
