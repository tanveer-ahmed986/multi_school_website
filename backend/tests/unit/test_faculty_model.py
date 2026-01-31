"""Unit tests for Faculty model (T018)."""
import uuid
import pytest
from src.models.faculty import Faculty


@pytest.mark.unit
class TestFacultyModel:
    def test_table_name(self):
        assert Faculty.__tablename__ == "faculty"

    def test_has_required_columns(self):
        assert hasattr(Faculty, "faculty_id")
        assert hasattr(Faculty, "school_id")
        assert hasattr(Faculty, "full_name")
        assert hasattr(Faculty, "designation")
        assert hasattr(Faculty, "qualification")
        assert hasattr(Faculty, "experience_years")

    def test_instantiate_with_required_fields(self):
        school_id = uuid.uuid4()
        f = Faculty(
            school_id=school_id,
            full_name="Jane Doe",
            designation="Teacher",
            qualification="M.Ed",
            experience_years=5,
        )
        assert f.school_id == school_id
        assert f.full_name == "Jane Doe"
        assert f.designation == "Teacher"
        assert f.experience_years == 5
        assert f.is_visible is True
        assert f.display_order == 0
