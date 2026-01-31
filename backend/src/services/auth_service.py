"""
Authentication service: login, refresh, logout, token rotation.
"""
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError

from src.models.user import User
from src.models.refresh_token import RefreshToken
from src.models.school import School
from src.utils.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_token_claims,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 15


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def get_user_by_email(db: Session, email: str, school_id: Optional[uuid.UUID] = None) -> Optional[User]:
    q = db.query(User).filter(User.email == email, User.is_active.is_(True))
    if school_id is not None:
        q = q.filter(User.school_id == school_id)
    return q.first()


def login(
    db: Session,
    email: str,
    password: str,
    school_id: Optional[uuid.UUID] = None,
) -> dict:
    """
    Authenticate user; return access_token, expires_in, user dict.
    Raises ValueError for invalid credentials.
    """
    user = get_user_by_email(db, email, school_id)
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")
    user_id = str(user.user_id)
    role = user.role
    user_school_id = str(user.school_id) if user.school_id else None
    access_token = create_access_token(subject=user_id, role=role, school_id=user_school_id)
    refresh_token = create_refresh_token(subject=user_id)
    expires_at = datetime.utcnow() + timedelta(days=7)
    rt = RefreshToken(
        user_id=user.user_id,
        token_hash=_hash_token(refresh_token),
        expires_at=expires_at,
    )
    db.add(rt)
    db.commit()
    user_dict = _user_to_dict(db, user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
        "user": user_dict,
    }


def _user_to_dict(db: Session, user: User) -> dict:
    schools = []
    if user.school_id:
        school = db.query(School).filter(School.school_id == user.school_id).first()
        if school:
            schools.append({
                "school_id": str(school.school_id),
                "school_name": school.school_name,
                "subdomain": school.subdomain,
            })
    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "role": user.role,
        "full_name": user.full_name,
        "schools": schools,
    }


def refresh(db: Session, refresh_token: str) -> dict:
    """
    Rotate refresh token; return new access_token and refresh_token.
    Revokes old refresh token. Raises ValueError if token invalid/expired/revoked.
    """
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise ValueError("Invalid refresh token")
    if not validate_token_claims(payload, expected_type="refresh"):
        raise ValueError("Invalid refresh token")
    token_hash = _hash_token(refresh_token)
    rt = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.is_revoked.is_(False),
    ).first()
    if not rt or rt.expires_at < datetime.utcnow():
        raise ValueError("Invalid or expired refresh token")
    user = db.query(User).filter(User.user_id == rt.user_id, User.is_active.is_(True)).first()
    if not user:
        raise ValueError("User not found")
    rt.is_revoked = True
    rt.revoked_at = datetime.utcnow()
    db.commit()
    user_id = str(user.user_id)
    role = user.role
    user_school_id = str(user.school_id) if user.school_id else None
    new_access = create_access_token(subject=user_id, role=role, school_id=user_school_id)
    new_refresh = create_refresh_token(subject=user_id)
    expires_at = datetime.utcnow() + timedelta(days=7)
    new_rt = RefreshToken(
        user_id=user.user_id,
        token_hash=_hash_token(new_refresh),
        expires_at=expires_at,
    )
    db.add(new_rt)
    db.commit()
    user_dict = _user_to_dict(db, user)
    return {
        "access_token": new_access,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": new_refresh,
        "user": user_dict,
    }


def logout(db: Session, refresh_token: str) -> None:
    """Revoke refresh token. No-op if token already invalid."""
    try:
        token_hash = _hash_token(refresh_token)
        rt = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
        if rt and not rt.is_revoked:
            rt.is_revoked = True
            rt.revoked_at = datetime.utcnow()
            db.commit()
    except Exception:
        pass
