/**
 * ThemeProvider component for dynamic theming.
 * (T180 - Implementation)
 *
 * Fetches school configuration and applies theme colors as CSS variables.
 * This enables dynamic branding across the entire application.
 */
'use client';

import { useEffect } from 'react';
import { useSchoolConfig } from '../../hooks/useSchoolConfig';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const { config, loading, error } = useSchoolConfig();

  useEffect(() => {
    if (config && !loading && !error) {
      // Update CSS variables for theme colors
      document.documentElement.style.setProperty(
        '--color-primary',
        config.primary_color || '#0A3D62'
      );
      document.documentElement.style.setProperty(
        '--color-secondary',
        config.secondary_color || '#EAF2F8'
      );
    }
  }, [config, loading, error]);

  return <>{children}</>;
}
