/**
 * usePermissions Hook
 *
 * Provides role-based permission checking for frontend components.
 * Used to conditionally render UI elements and protect routes.
 */

import { useAuth } from './useAuth';
import { UserRole } from '@/types/User';

interface Permissions {
  canAccessFaculty: boolean;
  canAccessResults: boolean;
  canAccessNotices: boolean;
  canAccessGallery: boolean;
  canAccessBranding: boolean;
  canAccessSuperAdmin: boolean;
  canManageSchools: boolean;
  canAssignAdmins: boolean;
}

/**
 * Hook to check user permissions based on role
 * @returns {Permissions} Object with permission flags
 */
export function usePermissions(): Permissions {
  const { user } = useAuth();

  if (!user) {
    return {
      canAccessFaculty: false,
      canAccessResults: false,
      canAccessNotices: false,
      canAccessGallery: false,
      canAccessBranding: false,
      canAccessSuperAdmin: false,
      canManageSchools: false,
      canAssignAdmins: false,
    };
  }

  const isSuperAdmin = user.role === UserRole.SUPER_ADMIN;
  const isSchoolAdmin = user.role === UserRole.SCHOOL_ADMIN;
  const isStaff = user.role === UserRole.STAFF;

  return {
    // Faculty management
    canAccessFaculty: isSuperAdmin || isSchoolAdmin,

    // Results management
    canAccessResults: isSuperAdmin || isSchoolAdmin,

    // Notices management
    canAccessNotices: isSuperAdmin || isSchoolAdmin || isStaff,

    // Gallery management
    canAccessGallery: isSuperAdmin || isSchoolAdmin || isStaff,

    // Branding/configuration
    canAccessBranding: isSuperAdmin || isSchoolAdmin,

    // Super admin panel
    canAccessSuperAdmin: isSuperAdmin,

    // School management
    canManageSchools: isSuperAdmin,

    // Admin assignment
    canAssignAdmins: isSuperAdmin,
  };
}

/**
 * Check if user has a specific permission
 * @param {keyof Permissions} permission - Permission to check
 * @returns {boolean} True if user has permission
 */
export function useHasPermission(permission: keyof Permissions): boolean {
  const permissions = usePermissions();
  return permissions[permission];
}
