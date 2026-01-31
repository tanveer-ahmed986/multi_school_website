"""
JWT utilities: create access/refresh tokens, decode, validate claims.
"""
import os
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production_32")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def create_access_token(
    subject: str,
    role: str,
    school_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token with sub, role, school_id, exp."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": subject,
        "role": role,
        "type": "access",
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    if school_id:
        payload["school_id"] = school_id
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token with sub, type=refresh, exp."""
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    payload = {
        "sub": subject,
        "type": "refresh",
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify JWT; raises JWTError if invalid or expired."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def validate_token_claims(payload: dict[str, Any], expected_type: str = "access") -> bool:
    """Return True if payload has expected type and required claims."""
    if payload.get("type") != expected_type:
        return False
    if "sub" not in payload or "exp" not in payload:
        return False
    return True


def hash_token(token: str) -> str:
    """Hash a token using SHA-256 for secure storage."""
    return hashlib.sha256(token.encode()).hexdigest()
