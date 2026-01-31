"""
Principal service - Business logic for principal profile management.
(T130 - Implementation)
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID

from src.models.principal import PrincipalProfile


class PrincipalService:
    """Service for managing principal profile (1:1 relationship with school)."""

    def __init__(self, db: Session, school_id: UUID):
        self.db = db
        self.school_id = school_id
        self.db.execute(text(f"SET app.current_school_id = '{school_id}'"))

    def upsert(self, profile_data: dict, updated_by: UUID) -> PrincipalProfile:
        """Create or update principal profile."""
        profile_data["school_id"] = self.school_id
        profile_data["updated_by"] = updated_by

        # Check if profile exists
        existing = self.db.query(PrincipalProfile).filter(
            PrincipalProfile.school_id == self.school_id
        ).first()

        if existing:
            # Update existing profile
            for key, value in profile_data.items():
                if hasattr(existing, key) and key != "school_id":
                    setattr(existing, key, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            # Create new profile
            profile = PrincipalProfile(**profile_data)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
            return profile

    def get(self) -> Optional[PrincipalProfile]:
        """Get principal profile for current school."""
        return self.db.query(PrincipalProfile).filter(
            PrincipalProfile.school_id == self.school_id
        ).first()
