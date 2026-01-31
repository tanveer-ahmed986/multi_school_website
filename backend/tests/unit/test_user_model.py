"""Unit tests for User model (T017)."""
import pytest
from src.models.user import User, UserRole


@pytest.mark.unit
class TestUserModel:
    def test_table_name(self):
        assert User.__tablename__ == "users"

    def test_has_required_columns(self):
        assert hasattr(User, "user_id")
        assert hasattr(User, "email")
        assert hasattr(User, "password_hash")
        assert hasattr(User, "role")
        assert hasattr(User, "full_name")

    def test_user_role_enum(self):
        assert UserRole.SUPER_ADMIN.value == "SUPER_ADMIN"
        assert UserRole.SCHOOL_ADMIN.value == "SCHOOL_ADMIN"
        assert UserRole.STAFF.value == "STAFF"

    def test_instantiate_with_required_fields(self):
        u = User(
            email="admin@platform.com",
            password_hash="$2b$12$fake",
            role=UserRole.SUPER_ADMIN.value,
            full_name="Platform Admin",
        )
        assert u.email == "admin@platform.com"
        assert u.role == "SUPER_ADMIN"
        assert u.full_name == "Platform Admin"
        assert u.school_id is None
        assert u.is_active is True
