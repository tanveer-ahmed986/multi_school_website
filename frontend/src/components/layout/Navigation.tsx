/**
 * Navigation Component
 *
 * Role-based navigation menu for admin panel.
 * Shows/hides menu items based on user permissions.
 * (T196, T197 - Accessibility improvements)
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { usePermissions } from '@/hooks/usePermissions';
import { useAuth } from '@/hooks/useAuth';

interface NavItem {
  href: string;
  label: string;
  permission: keyof ReturnType<typeof usePermissions>;
}

const NAV_ITEMS: NavItem[] = [
  { href: '/admin/dashboard', label: 'Dashboard', permission: 'canAccessBranding' },
  { href: '/admin/faculty', label: 'Faculty', permission: 'canAccessFaculty' },
  { href: '/admin/results', label: 'Results', permission: 'canAccessResults' },
  { href: '/admin/notices', label: 'Notices', permission: 'canAccessNotices' },
  { href: '/admin/gallery', label: 'Gallery', permission: 'canAccessGallery' },
  { href: '/admin/branding', label: 'Branding', permission: 'canAccessBranding' },
  { href: '/admin/principal', label: 'Principal', permission: 'canAccessBranding' },
  { href: '/admin/super-admin', label: 'Super Admin', permission: 'canAccessSuperAdmin' },
];

export function Navigation() {
  const pathname = usePathname();
  const permissions = usePermissions();
  const { user, logout } = useAuth();

  // Filter nav items based on permissions
  const visibleItems = NAV_ITEMS.filter((item) => permissions[item.permission]);

  if (!user) {
    return null;
  }

  return (
    <nav
      className="bg-white shadow-sm border-b"
      role="navigation"
      aria-label="Admin panel navigation"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex space-x-8" role="menubar">
            {visibleItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  role="menuitem"
                  aria-current={isActive ? 'page' : undefined}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                    isActive
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700" aria-label={`Logged in as ${user.email} with role ${user.role}`}>
              {user.email} ({user.role})
            </span>
            <button
              onClick={logout}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
              aria-label="Logout from admin panel"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
