"""
Tenant middleware: extract subdomain from Host, resolve school_id, set request state.
"""
from typing import Optional, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from src.database.connection import SessionLocal
from src.models.school import School


def extract_subdomain(host: str, base_domain: Optional[str] = None) -> Optional[str]:
    """
    Extract subdomain from host (e.g. springfield.localhost -> springfield).
    If base_domain is None, treat last two parts as base (localhost, example.com).
    """
    if not host or ":" in host:
        host = host.split(":")[0] if host else ""
    parts = host.lower().split(".")
    if len(parts) < 2:
        return None
    if base_domain:
        if not host.endswith(base_domain):
            return None
        sub = host[: -(len(base_domain) + 1)].strip(".")
        return sub if sub and sub != "www" else None
    if parts[-1] in ("localhost", "local"):
        if len(parts) >= 2 and parts[-2] == "localhost":
            return None
        return parts[0] if len(parts) >= 2 else None
    if len(parts) >= 3:
        return parts[0] if parts[0] != "www" else (parts[1] if len(parts) > 3 else None)
    return None


def resolve_school_id_by_subdomain(db: Session, subdomain: str):
    """Return school_id UUID for subdomain, or None."""
    school = db.query(School).filter(School.subdomain == subdomain, School.is_active.is_(True)).first()
    return school.school_id if school else None


class TenantMiddleware(BaseHTTPMiddleware):
    """Set request.state.school_id and request.state.subdomain from Host subdomain."""

    def __init__(self, app, base_domain: Optional[str] = None):
        super().__init__(app)
        self.base_domain = base_domain

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request.state.school_id = None
        request.state.subdomain = None
        host = request.headers.get("host") or ""
        subdomain = extract_subdomain(host, self.base_domain)
        if subdomain:
            request.state.subdomain = subdomain
            db = SessionLocal()
            try:
                school_id = resolve_school_id_by_subdomain(db, subdomain)
                if school_id:
                    request.state.school_id = school_id
            finally:
                db.close()
        return await call_next(request)
