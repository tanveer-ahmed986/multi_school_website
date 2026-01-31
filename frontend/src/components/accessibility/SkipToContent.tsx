/**
 * Skip to Content Component (T199)
 *
 * Provides skip navigation links for screen readers and keyboard users.
 * WCAG 2.1 Level AA requirement.
 */

'use client';

export function SkipToContent() {
  return (
    <div className="skip-to-content">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-md focus:shadow-lg"
      >
        Skip to main content
      </a>
      <a
        href="#navigation"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-40 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-md focus:shadow-lg"
      >
        Skip to navigation
      </a>
    </div>
  );
}
