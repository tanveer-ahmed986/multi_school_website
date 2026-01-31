"""Unit tests for Notice model (T020)."""
import uuid
import pytest
from src.models.notice import Notice


@pytest.mark.unit
class TestNoticeModel:
    def test_table_name(self):
        assert Notice.__tablename__ == "notices"

    def test_has_required_columns(self):
        assert hasattr(Notice, "notice_id")
        assert hasattr(Notice, "school_id")
        assert hasattr(Notice, "title")
        assert hasattr(Notice, "description")
        assert hasattr(Notice, "priority_level")
        assert hasattr(Notice, "expiry_date")
        assert hasattr(Notice, "created_by")

    def test_instantiate_with_required_fields(self):
        school_id = uuid.uuid4()
        user_id = uuid.uuid4()
        n = Notice(
            school_id=school_id,
            title="Holiday Notice",
            description="School closed on Monday.",
            created_by=user_id,
        )
        assert n.school_id == school_id
        assert n.title == "Holiday Notice"
        assert n.description == "School closed on Monday."
        assert n.priority_level == 0
        assert n.category == "general"
        assert n.is_published is False
        assert n.expiry_date is None
