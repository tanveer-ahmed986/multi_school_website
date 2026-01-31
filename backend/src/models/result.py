"""
Student result model. JSONB result_data; tenant-scoped by school_id.
"""
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.connection import Base


class Result(Base):
    __tablename__ = "results"

    result_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.school_id", ondelete="CASCADE"), nullable=False, index=True)
    academic_year = Column(String(20), nullable=False)
    class_level = Column(String(50), nullable=False)
    exam_type = Column(String(100), nullable=False)
    result_data = Column(JSONB, nullable=False)
    published_date = Column(DateTime(timezone=True), server_default=func.now())
    is_published = Column(Boolean, default=False, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    school = relationship("School", backref="results", foreign_keys=[school_id])
    creator = relationship("User", backref="created_results", foreign_keys=[created_by])
