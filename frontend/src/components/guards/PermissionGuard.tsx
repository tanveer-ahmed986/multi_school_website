/**
 * Permission Guard Component
 *
 * Protects routes based on user permissions.
 * Redirects to 403 page if user lacks required permission.
 */

'use client';

import { useRouter } from 'next/navigation';
import { useEffect, ReactNode } from 'react';
import { usePermissions } from '@/hooks/usePermissions';
import { useAuth } from '@/hooks/useAuth';

interface PermissionGuardProps {
  children: ReactNode;
  permission: keyof ReturnType<typeof usePermissions>;
  fallbackUrl?: string;
}

export function PermissionGuard({
  children,
  permission,
  fallbackUrl = '/403',
}: PermissionGuardProps) {
  const permissions = usePermissions();
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && user && !permissions[permission]) {
      router.push(fallbackUrl);
    }
  }, [user, isLoading, permissions, permission, fallbackUrl, router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!user || !permissions[permission]) {
    return null;
  }

  return <>{children}</>;
}
