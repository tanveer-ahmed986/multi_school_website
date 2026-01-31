"""
Principal profile model. 1:1 with school; tenant-scoped.
"""
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.connection import Base


class PrincipalProfile(Base):
    __tablename__ = "principal_profiles"

    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.school_id", ondelete="CASCADE"), primary_key=True)
    principal_name = Column(String(255), nullable=False)
    photo_url = Column(Text, nullable=True)
    message_text = Column(Text, nullable=False)
    qualification = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    school = relationship("School", backref="principal_profile", uselist=False, foreign_keys=[school_id])
    updater = relationship("User", backref="updated_principal_profiles", foreign_keys=[updated_by])
