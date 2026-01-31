"""
Gallery service - Business logic for gallery image management.
(T124 - Implementation)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID

from src.models.gallery import GalleryImage
from src.models.school import School


class GalleryService:
    """Service for managing gallery images with storage tracking."""

    def __init__(self, db: Session, school_id: UUID):
        self.db = db
        self.school_id = school_id
        self.db.execute(text(f"SET app.current_school_id = '{school_id}'"))

    def create(self, image_data: dict, uploaded_by: UUID) -> GalleryImage:
        """Upload image and update storage usage."""
        image_data["school_id"] = self.school_id
        image_data["uploaded_by"] = uploaded_by

        # Check storage limit
        school = self.db.query(School).filter(School.school_id == self.school_id).first()
        file_size = image_data.get("file_size_bytes", 0)

        if school.storage_used_bytes + file_size > school.storage_limit_bytes:
            raise ValueError(f"Storage limit exceeded. Available: {school.storage_limit_bytes - school.storage_used_bytes} bytes")

        image = GalleryImage(**image_data)
        self.db.add(image)

        # Update school storage usage
        school.storage_used_bytes += file_size
        self.db.commit()
        self.db.refresh(image)

        return image

    def delete(self, image_id: UUID) -> bool:
        """Delete image and decrement storage usage."""
        image = self.db.query(GalleryImage).filter(GalleryImage.image_id == image_id).first()

        if not image:
            return False

        # Decrement storage usage
        school = self.db.query(School).filter(School.school_id == self.school_id).first()
        school.storage_used_bytes = max(0, school.storage_used_bytes - image.file_size_bytes)

        self.db.delete(image)
        self.db.commit()

        return True
