"""
Notice service - Business logic for notices/announcements management.
(T118 - Implementation)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from datetime import datetime

from src.models.notice import Notice


class NoticeService:
    """Service for managing notices with tenant isolation."""

    def __init__(self, db: Session, school_id: UUID):
        self.db = db
        self.school_id = school_id
        self.db.execute(text(f"SET app.current_school_id = '{school_id}'"))

    def create(self, notice_data: dict, created_by: UUID) -> Notice:
        """Create a new notice with expiry validation."""
        notice_data["school_id"] = self.school_id
        notice_data["created_by"] = created_by

        # Validate expiry date is in future
        if notice_data.get("expiry_date"):
            expiry = notice_data["expiry_date"]
            if isinstance(expiry, str):
                expiry = datetime.fromisoformat(expiry)
            if expiry <= datetime.now():
                raise ValueError("Expiry date must be in the future")

        notice = Notice(**notice_data)
        self.db.add(notice)
        self.db.commit()
        self.db.refresh(notice)

        return notice

    def update(self, notice_id: UUID, update_data: dict) -> Optional[Notice]:
        """Update notice."""
        notice = self.db.query(Notice).filter(Notice.notice_id == notice_id).first()

        if not notice:
            return None

        # Validate expiry date if being updated
        if "expiry_date" in update_data and update_data["expiry_date"]:
            expiry = update_data["expiry_date"]
            if isinstance(expiry, str):
                expiry = datetime.fromisoformat(expiry)
            if expiry <= datetime.now():
                raise ValueError("Expiry date must be in the future")

        for key, value in update_data.items():
            if hasattr(notice, key) and key not in ["notice_id", "school_id", "created_by"]:
                setattr(notice, key, value)

        self.db.commit()
        self.db.refresh(notice)

        return notice
