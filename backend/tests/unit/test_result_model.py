"""Unit tests for Result model (T019)."""
import uuid
import pytest
from src.models.result import Result


@pytest.mark.unit
class TestResultModel:
    def test_table_name(self):
        assert Result.__tablename__ == "results"

    def test_has_required_columns(self):
        assert hasattr(Result, "result_id")
        assert hasattr(Result, "school_id")
        assert hasattr(Result, "academic_year")
        assert hasattr(Result, "class_level")
        assert hasattr(Result, "exam_type")
        assert hasattr(Result, "result_data")
        assert hasattr(Result, "created_by")

    def test_instantiate_with_required_fields(self):
        school_id = uuid.uuid4()
        user_id = uuid.uuid4()
        result_data = {"students": [], "statistics": {"total_students": 0}}
        r = Result(
            school_id=school_id,
            academic_year="2024-25",
            class_level="Class 10",
            exam_type="Annual",
            result_data=result_data,
            created_by=user_id,
        )
        assert r.school_id == school_id
        assert r.academic_year == "2024-25"
        assert r.class_level == "Class 10"
        assert r.result_data == result_data
        assert r.is_published is False
