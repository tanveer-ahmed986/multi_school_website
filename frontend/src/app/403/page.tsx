/**
 * 403 Access Denied Page
 *
 * Displayed when user tries to access a resource they don't have permission for.
 */

'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function AccessDeniedPage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full text-center">
        {/* 403 Icon */}
        <div className="mb-8">
          <svg
            className="mx-auto h-24 w-24 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>

        {/* Error Message */}
        <h1 className="text-6xl font-bold text-gray-900 mb-4">403</h1>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Access Denied</h2>
        <p className="text-gray-600 mb-8">
          You don&apos;t have permission to access this page. This resource is restricted to users
          with higher privileges.
        </p>

        {user && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
            <p className="text-sm text-yellow-800">
              <strong>Current Role:</strong> {user.role}
            </p>
            <p className="text-xs text-yellow-700 mt-1">
              Contact your administrator to request access to this feature.
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="space-y-3">
          <Link
            href={user ? '/admin/dashboard' : '/'}
            className="block w-full px-6 py-3 text-center text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
          >
            {user ? 'Back to Dashboard' : 'Go to Homepage'}
          </Link>
          <Link
            href="/admin/login"
            className="block w-full px-6 py-3 text-center text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50 transition-colors"
          >
            Login with Different Account
          </Link>
        </div>
      </div>
    </div>
  );
}
