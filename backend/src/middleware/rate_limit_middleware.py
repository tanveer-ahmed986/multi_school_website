"""
Rate limit middleware: throttle requests per client (e.g. per IP).
"""
import os
import time
from typing import Callable, Dict, Tuple
from collections import defaultdict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

# In-memory store: key -> (count, window_start). For production use Redis.
_store: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, 0.0))


def check_rate_limit(
    store: Dict[str, Tuple[int, float]],
    key: str,
    max_requests: int = RATE_LIMIT_PER_MINUTE,
    window_seconds: int = 60,
) -> bool:
    """Return True if under limit (and increment), False if over limit."""
    now = time.monotonic()
    count, start = store[key]
    if now - start >= window_seconds:
        store[key] = (1, now)
        return True
    if count >= max_requests:
        return False
    store[key] = (count + 1, start)
    return True


def get_client_key(request: Request) -> str:
    """Use X-Forwarded-For if present, else client host."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return "ip:" + forwarded.split(",")[0].strip()
    return "ip:" + (request.client.host if request.client else "unknown")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Reject request with 429 if client exceeds max_requests per window."""

    def __init__(self, app, max_requests: int = RATE_LIMIT_PER_MINUTE, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._store = _store

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        key = get_client_key(request)
        if not check_rate_limit(self._store, key, self.max_requests, self.window_seconds):
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=429, content={"detail": "Too many requests"})
        return await call_next(request)
