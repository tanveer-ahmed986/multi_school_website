"""Unit tests for PrincipalProfile model (T022)."""
import uuid
import pytest
from src.models.principal import PrincipalProfile


@pytest.mark.unit
class TestPrincipalProfileModel:
    def test_table_name(self):
        assert PrincipalProfile.__tablename__ == "principal_profiles"

    def test_has_required_columns(self):
        assert hasattr(PrincipalProfile, "school_id")
        assert hasattr(PrincipalProfile, "principal_name")
        assert hasattr(PrincipalProfile, "message_text")
        assert hasattr(PrincipalProfile, "updated_by")

    def test_school_id_is_primary_key(self):
        pk = PrincipalProfile.__table__.primary_key
        assert "school_id" in [c.name for c in pk.columns]

    def test_instantiate_with_required_fields(self):
        school_id = uuid.uuid4()
        user_id = uuid.uuid4()
        p = PrincipalProfile(
            school_id=school_id,
            principal_name="Dr. Smith",
            message_text="Welcome to our school.",
            updated_by=user_id,
        )
        assert p.school_id == school_id
        assert p.principal_name == "Dr. Smith"
        assert p.message_text == "Welcome to our school."
        assert p.updated_by == user_id
        assert p.photo_url is None
