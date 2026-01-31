"""
Gallery image model. Tenant-scoped by school_id; file tracking.
"""
import uuid
from datetime import date
from sqlalchemy import Column, String, Integer, Boolean, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.connection import Base


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.school_id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    image_url = Column(Text, nullable=False)
    thumbnail_url = Column(Text, nullable=True)
    caption = Column(Text, nullable=True)
    event_date = Column(Date, nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    school = relationship("School", backref="gallery_images", foreign_keys=[school_id])
    uploader = relationship("User", backref="uploaded_gallery_images", foreign_keys=[uploaded_by])
