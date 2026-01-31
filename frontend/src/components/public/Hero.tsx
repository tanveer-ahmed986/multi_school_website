/**
 * Hero section component for homepage.
 * (T085 - Implementation)
 */
'use client';

import React from 'react';
import { useSchoolConfig } from '../../hooks/useSchoolConfig';

export function Hero() {
  const { config, loading } = useSchoolConfig();

  if (loading) {
    return (
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <div className="h-12 bg-blue-700 animate-pulse rounded mb-4 mx-auto max-w-md"></div>
          <div className="h-6 bg-blue-700 animate-pulse rounded mx-auto max-w-sm"></div>
        </div>
      </section>
    );
  }

  const primaryColor = config?.primary_color || '#0A3D62';
  const secondaryColor = config?.secondary_color || '#EAF2F8';

  return (
    <section
      className="text-white py-20"
      style={{
        background: `linear-gradient(135deg, ${primaryColor} 0%, ${primaryColor}dd 100%)`,
      }}
    >
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          {config?.school_name || 'Welcome to Our School'}
        </h1>
        <p className="text-xl md:text-2xl text-gray-100">
          Excellence in Education, Building Future Leaders
        </p>
      </div>
    </section>
  );
}
