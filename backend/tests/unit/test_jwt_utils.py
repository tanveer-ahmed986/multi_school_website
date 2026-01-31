"""Unit tests for JWT utilities (T037)."""
import uuid
import pytest
from src.utils.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_token_claims,
)


@pytest.mark.unit
class TestJwtUtils:
    def test_create_access_token_returns_string(self):
        token = create_access_token(
            subject=str(uuid.uuid4()),
            role="SCHOOL_ADMIN",
            school_id=str(uuid.uuid4()),
        )
        assert isinstance(token, str)
        assert len(token) > 20

    def test_decode_token_returns_claims(self):
        user_id = str(uuid.uuid4())
        school_id = str(uuid.uuid4())
        token = create_access_token(subject=user_id, role="SCHOOL_ADMIN", school_id=school_id)
        payload = decode_token(token)
        assert payload["sub"] == user_id
        assert payload["role"] == "SCHOOL_ADMIN"
        assert payload.get("school_id") == school_id
        assert "exp" in payload

    def test_decode_invalid_token_raises(self):
        with pytest.raises(Exception):
            decode_token("invalid.jwt.token")

    def test_create_refresh_token_has_type_refresh(self):
        token = create_refresh_token(subject=str(uuid.uuid4()))
        payload = decode_token(token)
        assert payload.get("type") == "refresh"

    def test_validate_token_claims_accepts_valid_access(self):
        user_id = str(uuid.uuid4())
        token = create_access_token(subject=user_id, role="SUPER_ADMIN", school_id=None)
        payload = decode_token(token)
        assert validate_token_claims(payload, expected_type="access") is True

    def test_validate_token_claims_rejects_wrong_type(self):
        token = create_refresh_token(subject=str(uuid.uuid4()))
        payload = decode_token(token)
        assert validate_token_claims(payload, expected_type="access") is False
