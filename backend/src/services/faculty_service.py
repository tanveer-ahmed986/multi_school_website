"""
Faculty service - Business logic for faculty management.

Handles CRUD operations for faculty members with RLS enforcement.
(T104 - Implementation)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID

from src.models.faculty import Faculty


class FacultyService:
    """Service for managing faculty members with tenant isolation."""

    def __init__(self, db: Session, school_id: UUID):
        """
        Initialize faculty service with database session and school context.

        Args:
            db: SQLAlchemy database session
            school_id: Current school ID for RLS context
        """
        self.db = db
        self.school_id = school_id

        # Set RLS context for tenant isolation
        self.db.execute(text(f"SET app.current_school_id = '{school_id}'"))

    def create(self, faculty_data: dict) -> Faculty:
        """
        Create a new faculty member.

        Args:
            faculty_data: Dictionary containing faculty information

        Returns:
            Created Faculty object

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Ensure school_id matches current context
        faculty_data["school_id"] = self.school_id

        faculty = Faculty(**faculty_data)
        self.db.add(faculty)
        self.db.commit()
        self.db.refresh(faculty)

        return faculty

    def get_by_id(self, faculty_id: UUID) -> Optional[Faculty]:
        """
        Get faculty member by ID.

        RLS ensures only faculty from current school are returned.

        Args:
            faculty_id: Faculty member UUID

        Returns:
            Faculty object or None if not found
        """
        return self.db.query(Faculty).filter(
            Faculty.faculty_id == faculty_id
        ).first()

    def list_all(self, include_hidden: bool = False) -> List[Faculty]:
        """
        List all faculty members for the current school.

        Args:
            include_hidden: If False, only return visible faculty

        Returns:
            List of Faculty objects
        """
        query = self.db.query(Faculty).filter(Faculty.school_id == self.school_id)

        if not include_hidden:
            query = query.filter(Faculty.is_visible == True)

        return query.order_by(Faculty.display_order).all()

    def update(self, faculty_id: UUID, update_data: dict) -> Optional[Faculty]:
        """
        Update faculty member.

        Args:
            faculty_id: Faculty member UUID
            update_data: Dictionary containing fields to update

        Returns:
            Updated Faculty object or None if not found

        Raises:
            ValueError: If trying to change school_id
        """
        faculty = self.get_by_id(faculty_id)

        if not faculty:
            return None

        # Prevent changing school_id
        if "school_id" in update_data and update_data["school_id"] != self.school_id:
            raise ValueError("Cannot change school_id")

        # Update fields
        for key, value in update_data.items():
            if hasattr(faculty, key):
                setattr(faculty, key, value)

        self.db.commit()
        self.db.refresh(faculty)

        return faculty

    def delete(self, faculty_id: UUID) -> bool:
        """
        Delete faculty member.

        Args:
            faculty_id: Faculty member UUID

        Returns:
            True if deleted, False if not found
        """
        faculty = self.get_by_id(faculty_id)

        if not faculty:
            return False

        self.db.delete(faculty)
        self.db.commit()

        return True

    def toggle_visibility(self, faculty_id: UUID) -> Optional[Faculty]:
        """
        Toggle faculty member visibility on public website.

        Args:
            faculty_id: Faculty member UUID

        Returns:
            Updated Faculty object or None if not found
        """
        faculty = self.get_by_id(faculty_id)

        if not faculty:
            return None

        faculty.is_visible = not faculty.is_visible
        self.db.commit()
        self.db.refresh(faculty)

        return faculty
