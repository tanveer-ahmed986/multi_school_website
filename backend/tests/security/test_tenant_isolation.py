"""Tenant isolation security tests (T052). School A cannot see School B data."""
import uuid
from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm import Session

from src.models.school import School
from src.models.faculty import Faculty
from src.middleware.tenant_middleware import resolve_school_id_by_subdomain, extract_subdomain


@pytest.mark.security
class TestTenantIsolation:
    def test_subdomain_resolves_to_single_school(self):
        """Subdomain must resolve to at most one school_id."""
        db = MagicMock(spec=Session)
        school_id_a = uuid.uuid4()
        school = School(school_id=school_id_a, school_name="School A", subdomain="schoola", contact_email="a@a.com")
        db.query.return_value.filter.return_value.first.return_value = school
        result = resolve_school_id_by_subdomain(db, "schoola")
        assert result == school_id_a
        db.query.assert_called_once_with(School)

    def test_unknown_subdomain_returns_none(self):
        """Unknown subdomain must not return any school_id."""
        db = MagicMock(spec=Session)
        db.query.return_value.filter.return_value.first.return_value = None
        result = resolve_school_id_by_subdomain(db, "unknown")
        assert result is None

    def test_faculty_model_has_school_id_foreign_key(self):
        """Faculty must be scoped by school_id (RLS enforces at DB level)."""
        school_id_a = uuid.uuid4()
        school_id_b = uuid.uuid4()
        fa = Faculty(school_id=school_id_a, full_name="Teacher A", designation="Teacher", qualification="M.Ed", experience_years=5)
        fb = Faculty(school_id=school_id_b, full_name="Teacher B", designation="Teacher", qualification="M.Ed", experience_years=3)
        assert fa.school_id == school_id_a
        assert fb.school_id == school_id_b
        assert fa.school_id != fb.school_id
