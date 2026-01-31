"""Unit tests for AuthService (T042)."""
import uuid
from unittest.mock import MagicMock, patch
import pytest
from src.services.auth_service import (
    verify_password,
    hash_password,
    get_user_by_email,
    login,
    refresh,
    logout,
)


@pytest.mark.unit
class TestAuthServicePassword:
    def test_hash_and_verify(self):
        pwd = "SecurePass123!"
        hashed = hash_password(pwd)
        assert hashed != pwd
        assert verify_password(pwd, hashed) is True
        assert verify_password("wrong", hashed) is False


@pytest.mark.unit
class TestAuthServiceLogin:
    def test_login_invalid_credentials_raises(self):
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(ValueError, match="Invalid email or password"):
            login(db, "nobody@example.com", "wrong")

    def test_login_valid_returns_tokens_and_user(self):
        from src.models.user import User
        user_id = uuid.uuid4()
        school_id = uuid.uuid4()
        user = User(
            user_id=user_id,
            email="admin@school.edu",
            password_hash=hash_password("Pass123!"),
            role="SCHOOL_ADMIN",
            school_id=school_id,
            full_name="Admin",
        )
        school = MagicMock()
        school.school_id = school_id
        school.school_name = "Test School"
        school.subdomain = "test"
        db = MagicMock()
        # get_user_by_email: query(User).filter().filter().first() -> user
        user_chain = MagicMock()
        user_chain.filter.return_value.filter.return_value.first.return_value = user
        # _user_to_dict: query(School).filter().first() -> school
        school_chain = MagicMock()
        school_chain.filter.return_value.first.return_value = school
        db.query.side_effect = [user_chain, school_chain]
        result = login(db, "admin@school.edu", "Pass123!", school_id=school_id)
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        assert "user" in result
        assert result["user"]["email"] == "admin@school.edu"
        assert result["user"]["role"] == "SCHOOL_ADMIN"


@pytest.mark.unit
class TestAuthServiceRefresh:
    def test_refresh_invalid_token_raises(self):
        db = MagicMock()
        with pytest.raises(ValueError, match="Invalid"):
            refresh(db, "invalid.jwt.token")


@pytest.mark.unit
class TestAuthServiceLogout:
    def test_logout_does_not_raise(self):
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        logout(db, "any.token")  # no raise
