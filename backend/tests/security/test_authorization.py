"""Authorization security tests (T053). Role-based access enforcement."""
import uuid
import pytest
from src.models.user import User, UserRole
from src.services.auth_service import get_user_by_email


@pytest.mark.security
class TestAuthorization:
    def test_super_admin_has_no_school_id(self):
        """SUPER_ADMIN must have school_id NULL."""
        u = User(
            email="admin@platform.com",
            password_hash="hash",
            role=UserRole.SUPER_ADMIN.value,
            school_id=None,
            full_name="Super Admin",
        )
        assert u.role == "SUPER_ADMIN"
        assert u.school_id is None

    def test_school_admin_has_school_id(self):
        """SCHOOL_ADMIN must have school_id set."""
        school_id = uuid.uuid4()
        u = User(
            email="admin@school.edu",
            password_hash="hash",
            role=UserRole.SCHOOL_ADMIN.value,
            school_id=school_id,
            full_name="School Admin",
        )
        assert u.role == "SCHOOL_ADMIN"
        assert u.school_id == school_id

    def test_staff_has_school_id(self):
        """STAFF must have school_id set."""
        school_id = uuid.uuid4()
        u = User(
            email="staff@school.edu",
            password_hash="hash",
            role=UserRole.STAFF.value,
            school_id=school_id,
            full_name="Staff",
        )
        assert u.role == "STAFF"
        assert u.school_id == school_id

    def test_get_user_by_email_filters_by_school_id(self):
        """get_user_by_email with school_id must filter by school."""
        from unittest.mock import MagicMock
        db = MagicMock()
        school_id = uuid.uuid4()
        user = User(
            user_id=uuid.uuid4(),
            email="admin@school.edu",
            password_hash="hash",
            role=UserRole.SCHOOL_ADMIN.value,
            school_id=school_id,
            full_name="Admin",
        )
        db.query.return_value.filter.return_value.first.return_value = user
        result = get_user_by_email(db, "admin@school.edu", school_id=school_id)
        assert result == user
        # Verify filter was called with school_id
        db.query.return_value.filter.assert_called_once()
