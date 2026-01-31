"""
Integration tests for public API endpoints.

Tests cover:
- T055: GET /public/school - School info retrieval
- T057: GET /public/faculty - Visible faculty only
- T059, T060: GET /public/results - Year/class filtering
- T063: GET /public/notices - Active notices sorted by priority
- T065: GET /public/gallery - Category filtering
- T067: GET /public/principal - Principal profile
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.models.school import School


@pytest.fixture
def test_school(db_session: Session):
    """Create a test school for public API tests."""
    school = School(
        school_name="Test High School",
        subdomain="test",
        logo_url="/data/schools/test-school-id/config/logo.png",
        primary_color="#0A3D62",
        secondary_color="#EAF2F8",
        contact_email="admin@testhigh.edu",
        contact_phone="+1-555-0100",
        address="123 Test Street, Test City, TS 12345",
        is_active=True
    )
    db_session.add(school)
    db_session.commit()
    db_session.refresh(school)
    return school


class TestPublicSchoolInfo:
    """Tests for GET /public/school endpoint (T055)."""

    def test_get_school_info_success(self, client: TestClient, test_school: School):
        """Test successful school info retrieval."""
        # Set subdomain header to identify tenant
        headers = {"Host": f"{test_school.subdomain}.domain.com"}

        response = client.get("/public/school", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["school_name"] == test_school.school_name
        assert data["subdomain"] == test_school.subdomain
        assert data["primary_color"] == test_school.primary_color
        assert data["secondary_color"] == test_school.secondary_color
        assert data["contact_email"] == test_school.contact_email
        assert data["contact_phone"] == test_school.contact_phone
        assert data["address"] == test_school.address
        assert data["logo_url"] == test_school.logo_url

    def test_get_school_info_invalid_subdomain(self, client: TestClient):
        """Test school info retrieval with non-existent subdomain."""
        headers = {"Host": "nonexistent.domain.com"}

        response = client.get("/public/school", headers=headers)

        assert response.status_code == 404
        assert "school not found" in response.json()["detail"].lower()

    def test_get_school_info_inactive_school(self, client: TestClient, db_session: Session):
        """Test school info retrieval for inactive school."""
        inactive_school = School(
            school_name="Inactive School",
            subdomain="inactive",
            contact_email="admin@inactive.edu",
            is_active=False
        )
        db_session.add(inactive_school)
        db_session.commit()

        headers = {"Host": f"{inactive_school.subdomain}.domain.com"}
        response = client.get("/public/school", headers=headers)

        assert response.status_code == 404
        assert "school not active" in response.json()["detail"].lower()

    def test_get_school_info_missing_host_header(self, client: TestClient):
        """Test school info retrieval without Host header."""
        response = client.get("/public/school")

        assert response.status_code == 400
        assert "host header required" in response.json()["detail"].lower()


class TestPublicFaculty:
    """Tests for GET /public/faculty endpoint (T057)."""

    def test_get_visible_faculty_only(self, client: TestClient, test_school: School, db_session: Session):
        """Test that only visible faculty are returned."""
        from src.models.faculty import Faculty

        # Create visible faculty
        visible_faculty = Faculty(
            school_id=test_school.school_id,
            full_name="John Doe",
            designation="Teacher",
            qualification="M.Sc. Mathematics",
            experience_years=5,
            subject="Mathematics",
            is_visible=True
        )

        # Create hidden faculty
        hidden_faculty = Faculty(
            school_id=test_school.school_id,
            full_name="Jane Smith",
            designation="Principal",
            qualification="Ph.D. Education",
            experience_years=15,
            is_visible=False
        )

        db_session.add_all([visible_faculty, hidden_faculty])
        db_session.commit()

        headers = {"Host": f"{test_school.subdomain}.domain.com"}
        response = client.get("/public/faculty", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["full_name"] == "John Doe"
        assert data[0]["designation"] == "Teacher"

    def test_get_faculty_empty_list(self, client: TestClient, test_school: School):
        """Test faculty retrieval when no faculty exist."""
        headers = {"Host": f"{test_school.subdomain}.domain.com"}
        response = client.get("/public/faculty", headers=headers)

        assert response.status_code == 200
        assert response.json() == []


class TestPublicResults:
    """Tests for GET /public/results endpoints (T059, T060)."""

    def test_get_results_list_with_filters(self, client: TestClient, test_school: School, db_session: Session):
        """Test results listing with year/class filtering."""
        from src.models.result import Result

        result_2024 = Result(
            school_id=test_school.school_id,
            academic_year="2024-25",
            class_level="Class 10",
            exam_type="Annual",
            result_data={"students": [], "statistics": {"total_students": 50}},
            is_published=True,
            created_by=test_school.school_id  # Placeholder
        )

        result_2023 = Result(
            school_id=test_school.school_id,
            academic_year="2023-24",
            class_level="Class 10",
            exam_type="Annual",
            result_data={"students": [], "statistics": {"total_students": 48}},
            is_published=True,
            created_by=test_school.school_id
        )

        db_session.add_all([result_2024, result_2023])
        db_session.commit()

        headers = {"Host": f"{test_school.subdomain}.domain.com"}

        # Test without filters - should return all published results
        response = client.get("/public/results", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Test with year filter
        response = client.get("/public/results?year=2024-25", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["academic_year"] == "2024-25"

        # Test with class filter
        response = client.get("/public/results?class_level=Class 10", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_specific_result(self, client: TestClient, test_school: School, db_session: Session):
        """Test specific result retrieval by year and class."""
        from src.models.result import Result

        result = Result(
            school_id=test_school.school_id,
            academic_year="2024-25",
            class_level="Class 10",
            exam_type="Annual",
            result_data={
                "students": [
                    {
                        "roll_number": "101",
                        "student_name": "Test Student",
                        "total_marks": 450,
                        "percentage": 90.0,
                        "grade": "A+"
                    }
                ],
                "statistics": {
                    "total_students": 1,
                    "pass_percentage": 100.0,
                    "highest_marks": 450
                }
            },
            is_published=True,
            created_by=test_school.school_id
        )
        db_session.add(result)
        db_session.commit()

        headers = {"Host": f"{test_school.subdomain}.domain.com"}
        response = client.get("/public/results/2024-25/Class%2010", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["academic_year"] == "2024-25"
        assert data["class_level"] == "Class 10"
        assert len(data["result_data"]["students"]) == 1
        assert data["result_data"]["statistics"]["total_students"] == 1


class TestPublicNotices:
    """Tests for GET /public/notices endpoint (T063)."""

    def test_get_active_notices_sorted_by_priority(self, client: TestClient, test_school: School, db_session: Session):
        """Test that only active notices are returned, sorted by priority."""
        from src.models.notice import Notice
        from datetime import datetime, timedelta

        # High priority notice
        high_priority = Notice(
            school_id=test_school.school_id,
            title="Urgent: Exam Schedule",
            description="Exams start next week.",
            priority_level=4,
            is_published=True,
            expiry_date=datetime.now() + timedelta(days=7),
            created_by=test_school.school_id
        )

        # Low priority notice
        low_priority = Notice(
            school_id=test_school.school_id,
            title="Library Hours",
            description="Library open 9-5.",
            priority_level=1,
            is_published=True,
            expiry_date=datetime.now() + timedelta(days=30),
            created_by=test_school.school_id
        )

        # Expired notice (should not appear)
        expired = Notice(
            school_id=test_school.school_id,
            title="Old Notice",
            description="This is expired.",
            priority_level=3,
            is_published=True,
            expiry_date=datetime.now() - timedelta(days=1),
            created_by=test_school.school_id
        )

        db_session.add_all([high_priority, low_priority, expired])
        db_session.commit()

        headers = {"Host": f"{test_school.subdomain}.domain.com"}
        response = client.get("/public/notices", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Expired notice excluded
        assert data[0]["title"] == "Urgent: Exam Schedule"  # High priority first
        assert data[1]["title"] == "Library Hours"


class TestPublicGallery:
    """Tests for GET /public/gallery endpoint (T065)."""

    def test_get_gallery_with_category_filter(self, client: TestClient, test_school: School, db_session: Session):
        """Test gallery retrieval with category filtering."""
        from src.models.gallery import GalleryImage

        sports_image = GalleryImage(
            school_id=test_school.school_id,
            category="sports",
            image_url="/data/schools/test/gallery/sports/image1.jpg",
            caption="Sports Day",
            is_visible=True,
            file_size_bytes=2048000,
            uploaded_by=test_school.school_id
        )

        cultural_image = GalleryImage(
            school_id=test_school.school_id,
            category="cultural",
            image_url="/data/schools/test/gallery/cultural/image2.jpg",
            caption="Annual Function",
            is_visible=True,
            file_size_bytes=3048000,
            uploaded_by=test_school.school_id
        )

        db_session.add_all([sports_image, cultural_image])
        db_session.commit()

        headers = {"Host": f"{test_school.subdomain}.domain.com"}

        # Test without filter
        response = client.get("/public/gallery", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Test with category filter
        response = client.get("/public/gallery?category=sports", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "sports"
        assert data[0]["caption"] == "Sports Day"


class TestPublicPrincipal:
    """Tests for GET /public/principal endpoint (T067)."""

    def test_get_principal_profile(self, client: TestClient, test_school: School, db_session: Session):
        """Test principal profile retrieval."""
        from src.models.principal import PrincipalProfile

        principal = PrincipalProfile(
            school_id=test_school.school_id,
            principal_name="Dr. John Principal",
            photo_url="/data/schools/test/principal/photo.jpg",
            message_text="Welcome to our school!",
            qualification="Ph.D. Education",
            email="principal@testhigh.edu",
            phone="+1-555-0200",
            updated_by=test_school.school_id
        )
        db_session.add(principal)
        db_session.commit()

        headers = {"Host": f"{test_school.subdomain}.domain.com"}
        response = client.get("/public/principal", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["principal_name"] == "Dr. John Principal"
        assert data["message_text"] == "Welcome to our school!"
        assert data["photo_url"] == "/data/schools/test/principal/photo.jpg"

    def test_get_principal_not_found(self, client: TestClient, test_school: School):
        """Test principal profile retrieval when no profile exists."""
        headers = {"Host": f"{test_school.subdomain}.domain.com"}
        response = client.get("/public/principal")

        assert response.status_code == 404
        assert "principal profile not found" in response.json()["detail"].lower()
