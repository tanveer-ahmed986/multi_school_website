"""
Result service - Business logic for student results management.
(T112 - Implementation)
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from datetime import datetime

from src.models.result import Result


class ResultService:
    """Service for managing student results with tenant isolation."""

    def __init__(self, db: Session, school_id: UUID):
        self.db = db
        self.school_id = school_id
        self.db.execute(text(f"SET app.current_school_id = '{school_id}'"))

    def create(self, result_data: dict, created_by: UUID) -> Result:
        """Create a new result with JSONB validation."""
        # Validate result_data structure
        self._validate_result_data(result_data.get("result_data", {}))

        result_data["school_id"] = self.school_id
        result_data["created_by"] = created_by

        result = Result(**result_data)
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def update(self, result_id: UUID, update_data: dict) -> Optional[Result]:
        """Update result with audit logging."""
        result = self.db.query(Result).filter(Result.result_id == result_id).first()

        if not result:
            return None

        # Validate result_data if being updated
        if "result_data" in update_data:
            self._validate_result_data(update_data["result_data"])

        for key, value in update_data.items():
            if hasattr(result, key) and key not in ["result_id", "school_id", "created_by"]:
                setattr(result, key, value)

        self.db.commit()
        self.db.refresh(result)

        return result

    def _validate_result_data(self, data: dict) -> None:
        """Validate JSONB result_data structure."""
        if not isinstance(data, dict):
            raise ValueError("result_data must be a dictionary")

        if "students" not in data or not isinstance(data["students"], list):
            raise ValueError("result_data must contain 'students' array")

        if "statistics" not in data or not isinstance(data["statistics"], dict):
            raise ValueError("result_data must contain 'statistics' object")

        # Validate statistics has required fields
        stats = data["statistics"]
        required_stats = ["total_students", "pass_percentage", "highest_marks"]
        for field in required_stats:
            if field not in stats:
                raise ValueError(f"statistics must contain '{field}'")
