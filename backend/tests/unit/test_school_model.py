"""Unit tests for School model (T016)."""
import pytest
from src.models.school import School


@pytest.mark.unit
class TestSchoolModel:
    def test_table_name(self):
        assert School.__tablename__ == "schools"

    def test_has_required_columns(self):
        assert hasattr(School, "school_id")
        assert hasattr(School, "school_name")
        assert hasattr(School, "subdomain")
        assert hasattr(School, "contact_email")

    def test_has_default_columns(self):
        assert hasattr(School, "primary_color")
        assert hasattr(School, "secondary_color")
        assert hasattr(School, "is_active")
        assert hasattr(School, "storage_used_bytes")
        assert hasattr(School, "storage_limit_bytes")
        assert hasattr(School, "config_json")

    def test_instantiate_with_required_fields(self):
        s = School(
            school_name="Test School",
            subdomain="test",
            contact_email="admin@test.edu",
        )
        assert s.school_name == "Test School"
        assert s.subdomain == "test"
        assert s.contact_email == "admin@test.edu"
        assert s.is_active is True
        assert s.primary_color == "#0A3D62"
        assert s.secondary_color == "#EAF2F8"
        assert s.storage_used_bytes == 0
        assert s.storage_limit_bytes == 10737418240
