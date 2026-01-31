"""
School service - Business logic for school management (Super Admin).

Handles school creation, onboarding workflow, and admin assignment.
(T160 - Implementation)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4, UUID
import os
from pathlib import Path

from src.models.school import School
from src.models.user import User, UserRole
from passlib.hash import bcrypt


class SchoolService:
    """Service for managing schools (Super Admin only)."""

    def __init__(self, db: Session):
        self.db = db

    def create_school(
        self,
        school_name: str,
        subdomain: str,
        contact_email: str,
        contact_phone: Optional[str] = None,
        address: Optional[str] = None,
        primary_color: str = "#0A3D62",
        secondary_color: str = "#EAF2F8",
    ) -> School:
        """
        Create a new school with complete onboarding workflow.

        Steps:
        1. Generate unique school_id
        2. Create school record
        3. Initialize folder structure
        4. Create default configuration

        Args:
            school_name: Official school name
            subdomain: Subdomain for school website
            contact_email: School contact email
            contact_phone: School contact phone
            address: School physical address
            primary_color: Brand primary color
            secondary_color: Brand secondary color

        Returns:
            Created School object

        Raises:
            ValueError: If subdomain already exists or invalid
        """
        # Validate subdomain is unique
        existing = self.db.query(School).filter(School.subdomain == subdomain).first()
        if existing:
            raise ValueError(f"Subdomain '{subdomain}' is already taken")

        # Validate subdomain format (lowercase alphanumeric and hyphens only)
        if not self._is_valid_subdomain(subdomain):
            raise ValueError("Subdomain must be lowercase alphanumeric with hyphens, 3-50 chars")

        # Generate school ID
        school_id = uuid4()

        # Create school record
        school = School(
            school_id=school_id,
            school_name=school_name,
            subdomain=subdomain,
            contact_email=contact_email,
            contact_phone=contact_phone,
            address=address,
            primary_color=primary_color,
            secondary_color=secondary_color,
            is_active=True,
        )

        self.db.add(school)
        self.db.commit()
        self.db.refresh(school)

        # Initialize folder structure
        self._initialize_folder_structure(school_id)

        return school

    def _is_valid_subdomain(self, subdomain: str) -> bool:
        """Validate subdomain format."""
        if len(subdomain) < 3 or len(subdomain) > 50:
            return False

        # Only lowercase alphanumeric and hyphens
        import re
        pattern = r'^[a-z0-9-]+$'
        return bool(re.match(pattern, subdomain))

    def _initialize_folder_structure(self, school_id: UUID) -> None:
        """
        Create folder structure for new school.

        Structure:
        /data/schools/{school_id}/
            ├── config/
            ├── faculty/
            ├── results/
            ├── gallery/
            ├── notices/
            └── principal/
        """
        base_path = Path("./data/schools") / str(school_id)

        folders = [
            "config",
            "faculty",
            "results",
            "gallery",
            "notices",
            "principal",
        ]

        for folder in folders:
            folder_path = base_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)

    def assign_school_admin(
        self,
        school_id: UUID,
        email: str,
        password: str,
        full_name: str,
    ) -> User:
        """
        Create and assign a school admin user.

        Args:
            school_id: School UUID
            email: Admin email
            password: Admin password (will be hashed)
            full_name: Admin full name

        Returns:
            Created User object

        Raises:
            ValueError: If school not found or email already exists for this school
        """
        # Verify school exists
        school = self.db.query(School).filter(School.school_id == school_id).first()
        if not school:
            raise ValueError(f"School with ID {school_id} not found")

        # Check if email already exists for this school
        existing_user = self.db.query(User).filter(
            User.email == email,
            User.school_id == school_id
        ).first()

        if existing_user:
            raise ValueError(f"User with email {email} already exists for this school")

        # Create school admin user
        admin_user = User(
            email=email,
            password_hash=bcrypt.hash(password),
            role=UserRole.SCHOOL_ADMIN,
            school_id=school_id,
            full_name=full_name,
            is_active=True,
        )

        self.db.add(admin_user)
        self.db.commit()
        self.db.refresh(admin_user)

        return admin_user

    def list_schools(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> List[School]:
        """
        List all schools with pagination and filtering.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for school name or subdomain
            is_active: Filter by active status

        Returns:
            List of School objects
        """
        query = self.db.query(School)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (School.school_name.ilike(search_term)) |
                (School.subdomain.ilike(search_term))
            )

        if is_active is not None:
            query = query.filter(School.is_active == is_active)

        return query.offset(skip).limit(limit).all()

    def get_school_by_id(self, school_id: UUID) -> Optional[School]:
        """Get school by ID."""
        return self.db.query(School).filter(School.school_id == school_id).first()

    def update_school(
        self,
        school_id: UUID,
        update_data: dict,
    ) -> Optional[School]:
        """
        Update school configuration.

        Args:
            school_id: School UUID
            update_data: Dictionary of fields to update

        Returns:
            Updated School object or None if not found
        """
        school = self.get_school_by_id(school_id)

        if not school:
            return None

        # Update allowed fields
        allowed_fields = [
            "school_name", "contact_email", "contact_phone", "address",
            "logo_url", "primary_color", "secondary_color", "is_active",
            "storage_limit_bytes"
        ]

        for key, value in update_data.items():
            if key in allowed_fields and hasattr(school, key):
                setattr(school, key, value)

        self.db.commit()
        self.db.refresh(school)

        return school

    def deactivate_school(self, school_id: UUID) -> bool:
        """
        Deactivate a school (soft delete).

        Args:
            school_id: School UUID

        Returns:
            True if deactivated, False if not found
        """
        school = self.get_school_by_id(school_id)

        if not school:
            return False

        school.is_active = False
        self.db.commit()

        return True
