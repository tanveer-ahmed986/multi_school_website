"""Unit tests for AuthMiddleware (T046)."""
from unittest.mock import MagicMock, patch
import uuid
import pytest
from fastapi import Request
from starlette.datastructures import Headers

from src.middleware.auth_middleware import AuthMiddleware, get_current_user_id_from_request


@pytest.mark.unit
class TestAuthMiddleware:
    def test_missing_authorization_does_not_set_user(self):
        request = MagicMock(spec=Request)
        request.headers = Headers({})
        request.state = MagicMock()
        user_id = get_current_user_id_from_request(request)
        assert user_id is None

    def test_bearer_token_valid_returns_user_id(self):
        request = MagicMock(spec=Request)
        uid = str(uuid.uuid4())
        request.headers = Headers({"authorization": "Bearer fake.jwt.token"})
        with patch("src.middleware.auth_middleware.decode_token") as decode:
            decode.return_value = {"sub": uid, "role": "SCHOOL_ADMIN", "type": "access"}
            user_id = get_current_user_id_from_request(request)
        assert user_id == uid

    def test_invalid_bearer_returns_none(self):
        request = MagicMock(spec=Request)
        request.headers = Headers({"authorization": "Bearer invalid"})
        request.state = MagicMock()
        with patch("src.middleware.auth_middleware.decode_token") as decode:
            decode.side_effect = Exception("invalid")
            user_id = get_current_user_id_from_request(request)
        assert user_id is None
