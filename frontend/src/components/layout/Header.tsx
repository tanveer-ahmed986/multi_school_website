/**
 * Header component with dynamic school branding.
 * (T083 - Implementation)
 * (T196, T197, T199, T200 - Accessibility improvements)
 */
'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useSchoolConfig } from '../../hooks/useSchoolConfig';
import { SkipToContent } from '../accessibility/SkipToContent';

export function Header() {
  const { config, loading } = useSchoolConfig();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/faculty', label: 'Faculty' },
    { href: '/results', label: 'Results' },
    { href: '/gallery', label: 'Gallery' },
    { href: '/notices', label: 'Notices' },
  ];

  if (loading) {
    return (
      <header className="bg-gray-100 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="h-12 bg-gray-200 animate-pulse rounded"></div>
        </div>
      </header>
    );
  }

  const primaryColor = config?.primary_color || '#0A3D62';

  return (
    <>
      {/* Skip to Content Links (T199) */}
      <SkipToContent />

      <header
        className="sticky top-0 z-50 shadow-md"
        style={{ backgroundColor: primaryColor }}
        role="banner"
      >
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Logo and School Name */}
            <Link href="/" className="flex items-center space-x-3 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 rounded">
              {config?.logo_url && (
                <Image
                  src={config.logo_url}
                  alt={`${config.school_name} logo`}
                  width={48}
                  height={48}
                  className="rounded"
                />
              )}
              <span className="text-white text-xl font-bold">
                {config?.school_name || 'School'}
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav
              id="navigation"
              className="hidden md:flex space-x-6"
              role="navigation"
              aria-label="Main navigation"
            >
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-white hover:text-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-white rounded px-2 py-1"
                >
                  {link.label}
                </Link>
              ))}
            </nav>

            {/* Mobile Menu Button */}
            <button
              data-testid="mobile-menu-button"
              className="md:hidden text-white focus:outline-none focus:ring-2 focus:ring-white rounded p-2"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label={mobileMenuOpen ? 'Close mobile menu' : 'Open mobile menu'}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-navigation"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                {mobileMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <nav
              id="mobile-navigation"
              data-testid="mobile-nav"
              className="md:hidden mt-4 pb-4 space-y-2"
              role="navigation"
              aria-label="Mobile navigation"
            >
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="block text-white hover:text-gray-200 py-2 focus:outline-none focus:ring-2 focus:ring-white rounded px-2"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          )}
        </div>
      </header>
    </>
  );
}
