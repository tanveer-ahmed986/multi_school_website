"""
Auth middleware: validate JWT from Authorization header, inject user context into request.state.
"""
from typing import Optional, Callable
from uuid import UUID

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError

from src.utils.jwt_utils import decode_token, validate_token_claims


def get_current_user_id_from_request(request: Request) -> Optional[str]:
    """Extract and validate JWT from Authorization: Bearer <token>; return sub (user_id) or None."""
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth[7:].strip()
    if not token:
        return None
    try:
        payload = decode_token(token)
        if not validate_token_claims(payload, expected_type="access"):
            return None
        return payload.get("sub")
    except JWTError:
        return None


def get_current_user_claims_from_request(request: Request) -> Optional[dict]:
    """Decode JWT and return full claims (sub, role, school_id) or None."""
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth[7:].strip()
    if not token:
        return None
    try:
        payload = decode_token(token)
        if not validate_token_claims(payload, expected_type="access"):
            return None
        return payload
    except JWTError:
        return None


class AuthMiddleware(BaseHTTPMiddleware):
    """Set request.state.current_user_id (and optionally role, school_id) from JWT."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request.state.current_user_id = None
        request.state.current_user_role = None
        request.state.current_school_id = None
        claims = get_current_user_claims_from_request(request)
        if claims:
            request.state.current_user_id = claims.get("sub")
            request.state.current_user_role = claims.get("role")
            request.state.current_school_id = claims.get("school_id")
        return await call_next(request)
