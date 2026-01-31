"""
CSRF middleware: validate CSRF token on state-changing methods.
"""
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


def validate_csrf_token(
    request: Request,
    token_validator: Callable[[str], bool],
    header_name: str = "x-csrf-token",
) -> bool:
    """Return True if method is safe or token is present and valid."""
    if request.method in SAFE_METHODS:
        return True
    token = request.headers.get(header_name)
    if not token:
        return False
    return token_validator(token)


class CSRFMiddleware(BaseHTTPMiddleware):
    """Validate CSRF token for POST/PUT/PATCH/DELETE. Uses request.state.csrf_validator if set."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        def default_validator(t: str) -> bool:
            return bool(t and len(t) >= 16)

        validator = getattr(request.state, "csrf_validator", None) or default_validator
        if not validate_csrf_token(request, validator):
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=403, content={"detail": "Invalid or missing CSRF token"})
        return await call_next(request)
