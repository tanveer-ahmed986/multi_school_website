"""
Integration tests for content management API endpoints.

Tests cover:
- T176: PUT /content/branding - Update logo, colors, contact info
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.school import School
from src.models.user import User, UserRole
from src.utils.jwt_utils import create_access_token


@pytest.fixture
def test_school_and_admin(db_session: Session):
    """Create a test school and admin user."""
    school = School(
        school_name="Test School",
        subdomain="testschool",
        contact_email="admin@testschool.edu",
        contact_phone="+1-555-0100",
        address="123 Test St, Test City, TS 12345",
        logo_url=None,
        primary_color="#0A3D62",
        secondary_color="#EAF2F8",
        is_active=True
    )
    db_session.add(school)
    db_session.commit()
    db_session.refresh(school)

    # Create admin user
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


@pytest.fixture
def admin_auth_headers(test_school_and_admin: dict):
    """Generate authorization headers for admin user."""
    admin = test_school_and_admin["admin"]
    access_token = create_access_token(
        data={"sub": admin.email, "school_id": str(admin.school_id), "role": admin.role.value}
    )
    return {"Authorization": f"Bearer {access_token}"}


class TestBrandingAPI:
    """Tests for PUT /content/branding endpoint (T176)."""

    def test_update_branding_logo_url(
        self, client: TestClient, test_school_and_admin: dict, admin_auth_headers: dict, db_session: Session
    ):
        """Test updating school logo URL."""
        school = test_school_and_admin["school"]

        response = client.put(
            "/content/branding",
            json={"logo_url": "https://cdn.example.com/schools/testschool/logo.png"},
            headers=admin_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["logo_url"] == "https://cdn.example.com/schools/testschool/logo.png"

        # Verify database update
        db_session.refresh(school)
        assert school.logo_url == "https://cdn.example.com/schools/testschool/logo.png"

    def test_update_branding_colors(
        self, client: TestClient, test_school_and_admin: dict, admin_auth_headers: dict, db_session: Session
    ):
        """Test updating primary and secondary colors."""
        school = test_school_and_admin["school"]

        response = client.put(
            "/content/branding",
            json={
                "primary_color": "#FF5733",
                "secondary_color": "#C70039"
            },
            headers=admin_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["primary_color"] == "#FF5733"
        assert data["secondary_color"] == "#C70039"

        # Verify database update
        db_session.refresh(school)
        assert school.primary_color == "#FF5733"
        assert school.secondary_color == "#C70039"

    def test_update_branding_contact_info(
        self, client: TestClient, test_school_and_admin: dict, admin_auth_headers: dict, db_session: Session
    ):
        """Test updating contact email, phone, and address."""
        school = test_school_and_admin["school"]

        response = client.put(
            "/content/branding",
            json={
                "contact_email": "newadmin@testschool.edu",
                "contact_phone": "+1-555-9999",
                "address": "456 New Ave, New City, NC 54321"
            },
            headers=admin_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["contact_email"] == "newadmin@testschool.edu"
        assert data["contact_phone"] == "+1-555-9999"
        assert data["address"] == "456 New Ave, New City, NC 54321"

        # Verify database update
        db_session.refresh(school)
        assert school.contact_email == "newadmin@testschool.edu"
        assert school.contact_phone == "+1-555-9999"
        assert school.address == "456 New Ave, New City, NC 54321"

    def test_update_branding_partial_update(
        self, client: TestClient, test_school_and_admin: dict, admin_auth_headers: dict, db_session: Session
    ):
        """Test partial update - only updating some fields."""
        school = test_school_and_admin["school"]
        original_email = school.contact_email

        response = client.put(
            "/content/branding",
            json={"primary_color": "#123456"},
            headers=admin_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["primary_color"] == "#123456"
        assert data["contact_email"] == original_email  # Should remain unchanged

        # Verify database
        db_session.refresh(school)
        assert school.primary_color == "#123456"
        assert school.contact_email == original_email

    def test_update_branding_invalid_color_format(
        self, client: TestClient, admin_auth_headers: dict
    ):
        """Test validation for invalid hex color format."""
        response = client.put(
            "/content/branding",
            json={"primary_color": "not-a-color"},
            headers=admin_auth_headers
        )

        assert response.status_code == 422  # Unprocessable Entity

    def test_update_branding_invalid_email(
        self, client: TestClient, admin_auth_headers: dict
    ):
        """Test validation for invalid email format."""
        response = client.put(
            "/content/branding",
            json={"contact_email": "invalid-email"},
            headers=admin_auth_headers
        )

        assert response.status_code == 422  # Unprocessable Entity

    def test_update_branding_unauthorized(self, client: TestClient):
        """Test branding update without authentication returns 401."""
        response = client.put(
            "/content/branding",
            json={"primary_color": "#FF5733"}
        )

        assert response.status_code == 401

    def test_update_branding_tenant_isolation(
        self, client: TestClient, db_session: Session, admin_auth_headers: dict
    ):
        """Test that admin can only update their own school's branding."""
        # Create a second school
        other_school = School(
            school_name="Other School",
            subdomain="otherschool",
            contact_email="admin@otherschool.edu",
            primary_color="#000000",
            is_active=True
        )
        db_session.add(other_school)
        db_session.commit()
        db_session.refresh(other_school)

        original_color = other_school.primary_color

        # Admin from test_school tries to update (should only affect their school)
        response = client.put(
            "/content/branding",
            json={"primary_color": "#FFFFFF"},
            headers=admin_auth_headers
        )

        assert response.status_code == 200

        # Verify other school was NOT affected
        db_session.refresh(other_school)
        assert other_school.primary_color == original_color
