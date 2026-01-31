"""
Unit tests for role-based permissions system.

Tests cover:
- T186: STAFF role access matrix
- Permission checking for different content types
- Role hierarchy and access control
"""
import pytest
from src.models.user import UserRole
from src.utils.permissions import check_permission, require_role


class TestRoleBasedPermissions:
    """Tests for role-based permission system (T186)."""

    def test_super_admin_has_all_permissions(self):
        """Test that SUPER_ADMIN role has access to all resources."""
        assert check_permission(UserRole.SUPER_ADMIN, 'schools', 'create')
        assert check_permission(UserRole.SUPER_ADMIN, 'schools', 'read')
        assert check_permission(UserRole.SUPER_ADMIN, 'schools', 'update')
        assert check_permission(UserRole.SUPER_ADMIN, 'schools', 'delete')
        assert check_permission(UserRole.SUPER_ADMIN, 'faculty', 'create')
        assert check_permission(UserRole.SUPER_ADMIN, 'results', 'create')
        assert check_permission(UserRole.SUPER_ADMIN, 'notices', 'create')
        assert check_permission(UserRole.SUPER_ADMIN, 'gallery', 'create')

    def test_school_admin_has_content_permissions(self):
        """Test that SCHOOL_ADMIN role has access to all content management."""
        assert check_permission(UserRole.SCHOOL_ADMIN, 'faculty', 'create')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'faculty', 'update')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'faculty', 'delete')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'results', 'create')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'results', 'update')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'notices', 'create')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'notices', 'update')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'gallery', 'create')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'gallery', 'delete')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'principal', 'update')
        assert check_permission(UserRole.SCHOOL_ADMIN, 'branding', 'update')

    def test_school_admin_cannot_manage_schools(self):
        """Test that SCHOOL_ADMIN cannot create or delete schools."""
        assert not check_permission(UserRole.SCHOOL_ADMIN, 'schools', 'create')
        assert not check_permission(UserRole.SCHOOL_ADMIN, 'schools', 'delete')

    def test_staff_can_access_notices(self):
        """Test that STAFF role can create and update notices."""
        assert check_permission(UserRole.STAFF, 'notices', 'create')
        assert check_permission(UserRole.STAFF, 'notices', 'read')
        assert check_permission(UserRole.STAFF, 'notices', 'update')
        assert check_permission(UserRole.STAFF, 'notices', 'delete')

    def test_staff_can_access_gallery(self):
        """Test that STAFF role can upload and manage gallery images."""
        assert check_permission(UserRole.STAFF, 'gallery', 'create')
        assert check_permission(UserRole.STAFF, 'gallery', 'read')
        assert check_permission(UserRole.STAFF, 'gallery', 'delete')

    def test_staff_cannot_access_faculty(self):
        """Test that STAFF role cannot manage faculty."""
        assert not check_permission(UserRole.STAFF, 'faculty', 'create')
        assert not check_permission(UserRole.STAFF, 'faculty', 'update')
        assert not check_permission(UserRole.STAFF, 'faculty', 'delete')

    def test_staff_cannot_access_results(self):
        """Test that STAFF role cannot manage student results."""
        assert not check_permission(UserRole.STAFF, 'results', 'create')
        assert not check_permission(UserRole.STAFF, 'results', 'update')
        assert not check_permission(UserRole.STAFF, 'results', 'delete')

    def test_staff_cannot_access_principal(self):
        """Test that STAFF role cannot update principal profile."""
        assert not check_permission(UserRole.STAFF, 'principal', 'update')

    def test_staff_cannot_access_branding(self):
        """Test that STAFF role cannot update school branding."""
        assert not check_permission(UserRole.STAFF, 'branding', 'update')

    def test_staff_cannot_manage_schools(self):
        """Test that STAFF role cannot manage schools."""
        assert not check_permission(UserRole.STAFF, 'schools', 'create')
        assert not check_permission(UserRole.STAFF, 'schools', 'update')
        assert not check_permission(UserRole.STAFF, 'schools', 'delete')

    def test_require_role_decorator_allows_correct_role(self):
        """Test that require_role decorator allows users with correct role."""
        # This will be tested in integration tests with actual endpoints
        # Unit test just verifies the decorator can be applied
        @require_role(UserRole.STAFF)
        def staff_only_function():
            return "success"

        assert callable(staff_only_function)

    def test_permission_matrix_completeness(self):
        """Test that all content types have defined permissions."""
        content_types = ['faculty', 'results', 'notices', 'gallery', 'principal', 'branding']
        actions = ['create', 'read', 'update', 'delete']

        for content_type in content_types:
            for action in actions:
                # Should not raise KeyError
                try:
                    check_permission(UserRole.SCHOOL_ADMIN, content_type, action)
                    check_permission(UserRole.STAFF, content_type, action)
                except KeyError:
                    pytest.fail(f"Permission not defined for {content_type}.{action}")


class TestStaffAccessMatrix:
    """Comprehensive access matrix tests for STAFF role (T186)."""

    def test_staff_access_summary(self):
        """Test complete access matrix for STAFF role."""
        staff_role = UserRole.STAFF

        # Allowed resources
        allowed = [
            ('notices', 'create'),
            ('notices', 'read'),
            ('notices', 'update'),
            ('notices', 'delete'),
            ('gallery', 'create'),
            ('gallery', 'read'),
            ('gallery', 'delete'),
        ]

        for resource, action in allowed:
            assert check_permission(staff_role, resource, action), \
                f"STAFF should have {action} access to {resource}"

        # Denied resources
        denied = [
            ('faculty', 'create'),
            ('faculty', 'update'),
            ('faculty', 'delete'),
            ('results', 'create'),
            ('results', 'update'),
            ('results', 'delete'),
            ('principal', 'update'),
            ('branding', 'update'),
            ('schools', 'create'),
            ('schools', 'update'),
            ('schools', 'delete'),
        ]

        for resource, action in denied:
            assert not check_permission(staff_role, resource, action), \
                f"STAFF should NOT have {action} access to {resource}"
