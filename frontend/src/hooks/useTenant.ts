/**
 * Custom hook to extract tenant (school) subdomain from hostname.
 * (T095 - Implementation)
 */
'use client';

import { useMemo } from 'react';

interface TenantInfo {
  subdomain: string | null;
  hostname: string;
  isLocalDevelopment: boolean;
}

/**
 * Extract subdomain from window.location.hostname.
 *
 * Examples:
 * - schoolA.domain.com -> "schoolA"
 * - localhost:3000 -> null (development)
 * - 127.0.0.1:3000 -> null (development)
 *
 * @returns TenantInfo object with subdomain and metadata
 */
export function useTenant(): TenantInfo {
  const tenantInfo = useMemo(() => {
    if (typeof window === 'undefined') {
      return {
        subdomain: null,
        hostname: '',
        isLocalDevelopment: true,
      };
    }

    const hostname = window.location.hostname;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1';

    // For local development, use environment variable or default
    if (isLocalhost) {
      const devSubdomain = process.env.NEXT_PUBLIC_DEV_SUBDOMAIN || null;
      return {
        subdomain: devSubdomain,
        hostname,
        isLocalDevelopment: true,
      };
    }

    // Extract subdomain (first part before first dot)
    const parts = hostname.split('.');
    const subdomain = parts.length > 1 ? parts[0] : null;

    return {
      subdomain,
      hostname,
      isLocalDevelopment: false,
    };
  }, []);

  return tenantInfo;
}
