/**
 * Footer component with school contact information.
 * (T084 - Implementation)
 */
'use client';

import React from 'react';
import { useSchoolConfig } from '../../hooks/useSchoolConfig';

export function Footer() {
  const { config, loading } = useSchoolConfig();

  if (loading) {
    return (
      <footer className="bg-gray-800 text-white py-8 mt-auto">
        <div className="container mx-auto px-4">
          <div className="h-20 bg-gray-700 animate-pulse rounded"></div>
        </div>
      </footer>
    );
  }

  return (
    <footer className="bg-gray-800 text-white py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* School Info */}
          <div>
            <h3 className="text-lg font-bold mb-3">{config?.school_name}</h3>
            {config?.address && (
              <p className="text-gray-300 text-sm">{config.address}</p>
            )}
          </div>

          {/* Contact Information */}
          <div>
            <h3 className="text-lg font-bold mb-3">Contact</h3>
            <div className="space-y-2 text-sm">
              {config?.email && (
                <p className="text-gray-300">
                  <span className="font-semibold">Email:</span>{' '}
                  <a
                    href={`mailto:${config.email}`}
                    className="hover:text-white transition-colors"
                  >
                    {config.email}
                  </a>
                </p>
              )}
              {config?.phone && (
                <p className="text-gray-300">
                  <span className="font-semibold">Phone:</span>{' '}
                  <a
                    href={`tel:${config.phone}`}
                    className="hover:text-white transition-colors"
                  >
                    {config.phone}
                  </a>
                </p>
              )}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-bold mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/faculty" className="text-gray-300 hover:text-white transition-colors">
                  Faculty
                </a>
              </li>
              <li>
                <a href="/results" className="text-gray-300 hover:text-white transition-colors">
                  Results
                </a>
              </li>
              <li>
                <a href="/gallery" className="text-gray-300 hover:text-white transition-colors">
                  Gallery
                </a>
              </li>
              <li>
                <a href="/notices" className="text-gray-300 hover:text-white transition-colors">
                  Notices
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700 text-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} {config?.school_name}. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
