"""
Integration tests for authentication API endpoints.

Tests cover:
- T097: POST /auth/login - Login success, invalid credentials, refresh token cookie
- T098: POST /auth/refresh - Token rotation, expired refresh token
- T099: POST /auth/logout - Token revocation
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.models.school import School
from src.models.user import User, UserRole
from src.models.refresh_token import RefreshToken
from src.utils.jwt_utils import create_access_token, create_refresh_token, hash_token


@pytest.fixture
def test_school_and_admin(db_session: Session):
    """Create a test school and admin user."""
    school = School(
        school_name="Test School",
        subdomain="testschool",
        contact_email="admin@testschool.edu",
        is_active=True
    )
    db_session.add(school)
    db_session.commit()
    db_session.refresh(school)

    # Create admin user with bcrypt hashed password
    from passlib.hash import bcrypt
    admin_user = User(
        email="admin@testschool.edu",
        password_hash=bcrypt.hash("SecurePassword123!"),
        role=UserRole.SCHOOL_ADMIN,
        school_id=school.school_id,
        full_name="Test Admin",
        is_active=True
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)

    return {"school": school, "admin": admin_user}


class TestAuthLogin:
    """Tests for POST /auth/login endpoint (T097)."""

    def test_login_success_returns_tokens(self, client: TestClient, test_school_and_admin: dict):
        """Test successful login returns access token and sets refresh token cookie."""
        response = client.post(
            "/auth/login",
            json={
                "email": "admin@testschool.edu",
                "password": "SecurePassword123!"
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Check access token is returned
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "admin@testschool.edu"
        assert data["user"]["role"] == "SCHOOL_ADMIN"

        # Check refresh token cookie is set
        assert "refresh_token" in response.cookies
        refresh_cookie = response.cookies["refresh_token"]
        assert refresh_cookie is not None

    def test_login_invalid_email(self, client: TestClient):
        """Test login with non-existent email returns 401."""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "anypassword"
            }
        )

        assert response.status_code == 401
        assert "invalid credentials" in response.json()["detail"].lower()

    def test_login_invalid_password(self, client: TestClient, test_school_and_admin: dict):
        """Test login with incorrect password returns 401."""
        response = client.post(
            "/auth/login",
            json={
                "email": "admin@testschool.edu",
                "password": "WrongPassword123!"
            }
        )

        assert response.status_code == 401
        assert "invalid credentials" in response.json()["detail"].lower()

    def test_login_inactive_user(self, client: TestClient, db_session: Session, test_school_and_admin: dict):
        """Test login with inactive user account returns 403."""
        admin = test_school_and_admin["admin"]
        admin.is_active = False
        db_session.commit()

        response = client.post(
            "/auth/login",
            json={
                "email": "admin@testschool.edu",
                "password": "SecurePassword123!"
            }
        )

        assert response.status_code == 403
        assert "account is inactive" in response.json()["detail"].lower()

    def test_login_missing_fields(self, client: TestClient):
        """Test login with missing fields returns 422."""
        response = client.post(
            "/auth/login",
            json={"email": "admin@testschool.edu"}
        )

        assert response.status_code == 422

    def test_login_updates_last_login(self, client: TestClient, db_session: Session, test_school_and_admin: dict):
        """Test that successful login updates user's last_login timestamp."""
        admin = test_school_and_admin["admin"]
        initial_last_login = admin.last_login

        response = client.post(
            "/auth/login",
            json={
                "email": "admin@testschool.edu",
                "password": "SecurePassword123!"
            }
        )

        assert response.status_code == 200

        # Refresh user from database
        db_session.refresh(admin)
        assert admin.last_login is not None
        assert admin.last_login != initial_last_login


class TestAuthRefresh:
    """Tests for POST /auth/refresh endpoint (T098)."""

    def test_refresh_with_valid_token_returns_new_access_token(
        self, client: TestClient, db_session: Session, test_school_and_admin: dict
    ):
        """Test refresh token rotation with valid refresh token."""
        admin = test_school_and_admin["admin"]

        # Create a valid refresh token
        refresh_token_value = create_refresh_token(str(admin.user_id))
        token_hash = hash_token(refresh_token_value)

        refresh_token_record = RefreshToken(
            user_id=admin.user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_revoked=False
        )
        db_session.add(refresh_token_record)
        db_session.commit()

        # Make refresh request with cookie
        response = client.post(
            "/auth/refresh",
            cookies={"refresh_token": refresh_token_value}
        )

        assert response.status_code == 200
        data = response.json()

        # Check new access token is returned
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        # Check new refresh token cookie is set
        assert "refresh_token" in response.cookies

        # Verify old refresh token is revoked
        db_session.refresh(refresh_token_record)
        assert refresh_token_record.is_revoked is True

    def test_refresh_with_missing_token_returns_401(self, client: TestClient):
        """Test refresh without refresh token returns 401."""
        response = client.post("/auth/refresh")

        assert response.status_code == 401
        assert "refresh token required" in response.json()["detail"].lower()

    def test_refresh_with_invalid_token_returns_401(self, client: TestClient):
        """Test refresh with invalid token format returns 401."""
        response = client.post(
            "/auth/refresh",
            cookies={"refresh_token": "invalid.token.format"}
        )

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_refresh_with_revoked_token_returns_401(
        self, client: TestClient, db_session: Session, test_school_and_admin: dict
    ):
        """Test refresh with revoked token returns 401."""
        admin = test_school_and_admin["admin"]

        # Create a revoked refresh token
        refresh_token_value = create_refresh_token(str(admin.user_id))
        token_hash = hash_token(refresh_token_value)

        refresh_token_record = RefreshToken(
            user_id=admin.user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_revoked=True  # Already revoked
        )
        db_session.add(refresh_token_record)
        db_session.commit()

        response = client.post(
            "/auth/refresh",
            cookies={"refresh_token": refresh_token_value}
        )

        assert response.status_code == 401
        assert "revoked" in response.json()["detail"].lower()

    def test_refresh_with_expired_token_returns_401(
        self, client: TestClient, db_session: Session, test_school_and_admin: dict
    ):
        """Test refresh with expired token returns 401."""
        admin = test_school_and_admin["admin"]

        # Create an expired refresh token
        refresh_token_value = create_refresh_token(str(admin.user_id))
        token_hash = hash_token(refresh_token_value)

        refresh_token_record = RefreshToken(
            user_id=admin.user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() - timedelta(days=1),  # Expired
            is_revoked=False
        )
        db_session.add(refresh_token_record)
        db_session.commit()

        response = client.post(
            "/auth/refresh",
            cookies={"refresh_token": refresh_token_value}
        )

        assert response.status_code == 401
        assert "expired" in response.json()["detail"].lower()


class TestAuthLogout:
    """Tests for POST /auth/logout endpoint (T099)."""

    def test_logout_revokes_refresh_token(
        self, client: TestClient, db_session: Session, test_school_and_admin: dict
    ):
        """Test logout revokes the refresh token."""
        admin = test_school_and_admin["admin"]

        # Create a valid refresh token
        refresh_token_value = create_refresh_token(str(admin.user_id))
        token_hash = hash_token(refresh_token_value)

        refresh_token_record = RefreshToken(
            user_id=admin.user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_revoked=False
        )
        db_session.add(refresh_token_record)
        db_session.commit()

        # Logout request with refresh token cookie
        response = client.post(
            "/auth/logout",
            cookies={"refresh_token": refresh_token_value}
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"

        # Verify refresh token is revoked
        db_session.refresh(refresh_token_record)
        assert refresh_token_record.is_revoked is True
        assert refresh_token_record.revoked_at is not None

    def test_logout_without_token_returns_401(self, client: TestClient):
        """Test logout without refresh token returns 401."""
        response = client.post("/auth/logout")

        assert response.status_code == 401
        assert "refresh token required" in response.json()["detail"].lower()

    def test_logout_with_invalid_token_returns_401(self, client: TestClient):
        """Test logout with invalid token returns 401."""
        response = client.post(
            "/auth/logout",
            cookies={"refresh_token": "invalid.token"}
        )

        assert response.status_code == 401

    def test_logout_clears_refresh_token_cookie(
        self, client: TestClient, db_session: Session, test_school_and_admin: dict
    ):
        """Test that logout clears the refresh token cookie."""
        admin = test_school_and_admin["admin"]

        # Create a valid refresh token
        refresh_token_value = create_refresh_token(str(admin.user_id))
        token_hash = hash_token(refresh_token_value)

        refresh_token_record = RefreshToken(
            user_id=admin.user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_revoked=False
        )
        db_session.add(refresh_token_record)
        db_session.commit()

        response = client.post(
            "/auth/logout",
            cookies={"refresh_token": refresh_token_value}
        )

        assert response.status_code == 200

        # Check that refresh_token cookie is cleared (max_age=0 or expires in past)
        set_cookie_header = response.headers.get("set-cookie", "")
        assert "refresh_token" in set_cookie_header
        # Cookie should be expired or have max-age=0
        assert "max-age=0" in set_cookie_header.lower() or "expires=" in set_cookie_header.lower()
