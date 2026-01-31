"""Unit tests for CSRFMiddleware (T047)."""
from unittest.mock import MagicMock, patch
import pytest
from fastapi import Request
from starlette.datastructures import Headers

from src.middleware.csrf_middleware import CSRFMiddleware, validate_csrf_token


@pytest.mark.unit
class TestCSRFMiddleware:
    def test_safe_methods_not_checked(self):
        request = MagicMock(spec=Request)
        request.method = "GET"
        request.headers = Headers({})
        assert validate_csrf_token(request, lambda x: True) is True

    def test_unsafe_method_missing_token_fails(self):
        request = MagicMock(spec=Request)
        request.method = "POST"
        request.headers = Headers({})
        assert validate_csrf_token(request, lambda x: False) is False

    def test_unsafe_method_valid_token_passes(self):
        request = MagicMock(spec=Request)
        request.method = "POST"
        request.headers = Headers({"x-csrf-token": "valid-token"})
        assert validate_csrf_token(request, lambda t: t == "valid-token") is True
