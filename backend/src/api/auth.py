"""
Authentication API endpoints.

Provides JWT-based authentication with refresh token rotation:
- POST /auth/login - Login with email/password, returns access token and sets refresh token cookie
- POST /auth/refresh - Rotate refresh token and issue new access token
- POST /auth/logout - Revoke refresh token

All endpoints follow security best practices for school platform authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
from passlib.hash import bcrypt

from src.database.connection import get_db
from src.models.user import User, UserRole
from src.models.refresh_token import RefreshToken
from src.utils.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_token_claims,
    hash_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class MessageResponse(BaseModel):
    message: str


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email and password.

    Returns access token in response body and sets HTTP-only refresh token cookie.
    (T100 - Implementation)

    Security measures:
    - Bcrypt password hashing
    - HTTP-only, Secure, SameSite cookies for refresh token
    - Short-lived access tokens (15 minutes)
    - Long-lived refresh tokens (7 days)
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not bcrypt.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if user is active
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    # Update last login timestamp
    user.last_login = datetime.utcnow()
    db.commit()

    # Create access token
    access_token = create_access_token(
        subject=str(user.user_id),
        role=user.role.value,
        school_id=str(user.school_id) if user.school_id else None
    )

    # Create refresh token
    refresh_token_value = create_refresh_token(subject=str(user.user_id))
    token_hash = hash_token(refresh_token_value)

    # Store refresh token in database
    refresh_token_record = RefreshToken(
        user_id=user.user_id,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(days=7),
        is_revoked=False
    )
    db.add(refresh_token_record)
    db.commit()

    # Set HTTP-only cookie with refresh token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token_value,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 days in seconds
    )

    return TokenResponse(
        access_token=access_token,
        user={
            "user_id": str(user.user_id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "school_id": str(user.school_id) if user.school_id else None
        }
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Rotate refresh token and issue new access token.

    Implements refresh token rotation for enhanced security:
    1. Validates current refresh token
    2. Revokes current refresh token
    3. Issues new refresh token
    4. Issues new access token

    (T101 - Implementation)
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    try:
        # Decode and validate refresh token
        payload = decode_token(refresh_token)
        if not validate_token_claims(payload, expected_type="refresh"):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload["sub"]

        # Find refresh token in database
        token_hash = hash_token(refresh_token)
        stored_token = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked == False
        ).first()

        if not stored_token:
            raise HTTPException(status_code=401, detail="Refresh token not found or revoked")

        # Check if token is expired
        if stored_token.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Get user
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")

        # Revoke old refresh token
        stored_token.is_revoked = True
        stored_token.revoked_at = datetime.utcnow()

        # Create new refresh token
        new_refresh_token_value = create_refresh_token(subject=str(user.user_id))
        new_token_hash = hash_token(new_refresh_token_value)

        new_refresh_token_record = RefreshToken(
            user_id=user.user_id,
            token_hash=new_token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_revoked=False
        )
        db.add(new_refresh_token_record)
        db.commit()

        # Create new access token
        access_token = create_access_token(
            subject=str(user.user_id),
            role=user.role.value,
            school_id=str(user.school_id) if user.school_id else None
        )

        # Set new refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token_value,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )

        return TokenResponse(
            access_token=access_token,
            user={
                "user_id": str(user.user_id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "school_id": str(user.school_id) if user.school_id else None
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {str(e)}")


@router.post("/logout", response_model=MessageResponse)
def logout(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Logout user by revoking refresh token.

    Revokes the refresh token in database and clears the cookie.
    (T102 - Implementation)
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token required")

    try:
        # Find and revoke refresh token
        token_hash = hash_token(refresh_token)
        stored_token = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked == False
        ).first()

        if stored_token:
            stored_token.is_revoked = True
            stored_token.revoked_at = datetime.utcnow()
            db.commit()

        # Clear refresh token cookie
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            samesite="lax"
        )

        return MessageResponse(message="Logged out successfully")

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Logout failed: {str(e)}")
