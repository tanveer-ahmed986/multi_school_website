/**
 * Unit Tests: usePermissions Hook
 *
 * Tests role-based permission checking logic
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { usePermissions } from '@/hooks/usePermissions';
import { useAuth } from '@/hooks/useAuth';
import { UserRole } from '@/types/User';

// Mock useAuth hook
vi.mock('@/hooks/useAuth');

describe('usePermissions', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('T192.1: No user (unauthenticated)', () => {
    it('should deny all permissions when user is null', () => {
      vi.mocked(useAuth).mockReturnValue({
        user: null,
        login: vi.fn(),
        logout: vi.fn(),
        isAuthenticated: false,
        isLoading: false,
      });

      const { result } = renderHook(() => usePermissions());

      expect(result.current.canAccessFaculty).toBe(false);
      expect(result.current.canAccessResults).toBe(false);
      expect(result.current.canAccessNotices).toBe(false);
      expect(result.current.canAccessGallery).toBe(false);
      expect(result.current.canAccessBranding).toBe(false);
      expect(result.current.canAccessSuperAdmin).toBe(false);
      expect(result.current.canManageSchools).toBe(false);
      expect(result.current.canAssignAdmins).toBe(false);
    });
  });

  describe('T192.2: Super Admin permissions', () => {
    it('should grant all permissions to SUPER_ADMIN', () => {
      vi.mocked(useAuth).mockReturnValue({
        user: {
          id: '1',
          email: 'superadmin@platform.com',
          role: UserRole.SUPER_ADMIN,
          schoolId: null,
        },
        login: vi.fn(),
        logout: vi.fn(),
        isAuthenticated: true,
        isLoading: false,
      });

      const { result } = renderHook(() => usePermissions());

      expect(result.current.canAccessFaculty).toBe(true);
      expect(result.current.canAccessResults).toBe(true);
      expect(result.current.canAccessNotices).toBe(true);
      expect(result.current.canAccessGallery).toBe(true);
      expect(result.current.canAccessBranding).toBe(true);
      expect(result.current.canAccessSuperAdmin).toBe(true);
      expect(result.current.canManageSchools).toBe(true);
      expect(result.current.canAssignAdmins).toBe(true);
    });
  });

  describe('T192.3: School Admin permissions', () => {
    it('should grant appropriate permissions to SCHOOL_ADMIN', () => {
      vi.mocked(useAuth).mockReturnValue({
        user: {
          id: '2',
          email: 'admin@schoola.com',
          role: UserRole.SCHOOL_ADMIN,
          schoolId: 'school-a-id',
        },
        login: vi.fn(),
        logout: vi.fn(),
        isAuthenticated: true,
        isLoading: false,
      });

      const { result } = renderHook(() => usePermissions());

      // Allowed permissions
      expect(result.current.canAccessFaculty).toBe(true);
      expect(result.current.canAccessResults).toBe(true);
      expect(result.current.canAccessNotices).toBe(true);
      expect(result.current.canAccessGallery).toBe(true);
      expect(result.current.canAccessBranding).toBe(true);

      // Denied permissions
      expect(result.current.canAccessSuperAdmin).toBe(false);
      expect(result.current.canManageSchools).toBe(false);
      expect(result.current.canAssignAdmins).toBe(false);
    });
  });

  describe('T192.4: Staff permissions (limited access)', () => {
    it('should grant only notices and gallery permissions to STAFF', () => {
      vi.mocked(useAuth).mockReturnValue({
        user: {
          id: '3',
          email: 'staff@schoola.com',
          role: UserRole.STAFF,
          schoolId: 'school-a-id',
        },
        login: vi.fn(),
        logout: vi.fn(),
        isAuthenticated: true,
        isLoading: false,
      });

      const { result } = renderHook(() => usePermissions());

      // Allowed permissions
      expect(result.current.canAccessNotices).toBe(true);
      expect(result.current.canAccessGallery).toBe(true);

      // Denied permissions
      expect(result.current.canAccessFaculty).toBe(false);
      expect(result.current.canAccessResults).toBe(false);
      expect(result.current.canAccessBranding).toBe(false);
      expect(result.current.canAccessSuperAdmin).toBe(false);
      expect(result.current.canManageSchools).toBe(false);
      expect(result.current.canAssignAdmins).toBe(false);
    });
  });

  describe('T192.5: Permission consistency', () => {
    it('should return consistent permissions for same role', () => {
      vi.mocked(useAuth).mockReturnValue({
        user: {
          id: '4',
          email: 'staff2@schoolb.com',
          role: UserRole.STAFF,
          schoolId: 'school-b-id',
        },
        login: vi.fn(),
        logout: vi.fn(),
        isAuthenticated: true,
        isLoading: false,
      });

      const { result: result1 } = renderHook(() => usePermissions());
      const { result: result2 } = renderHook(() => usePermissions());

      expect(result1.current).toEqual(result2.current);
    });
  });
});
