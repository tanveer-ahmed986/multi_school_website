/**
 * Principal message component for homepage.
 */
'use client';

import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { publicService } from '../../services/publicService';
import type { PrincipalProfile } from '../../types/Principal';

export function PrincipalMessage() {
  const [principal, setPrincipal] = useState<PrincipalProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPrincipal = async () => {
      try {
        const data = await publicService.getPrincipal();
        setPrincipal(data);
      } catch (error) {
        console.error('Failed to fetch principal profile:', error);
        setPrincipal(null);
      } finally {
        setLoading(false);
      }
    };

    fetchPrincipal();
  }, []);

  if (loading) {
    return (
      <div data-testid="principal-message" className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex items-center space-x-6 mb-6">
          <div className="w-24 h-24 rounded-full bg-gray-200 animate-pulse"></div>
          <div className="flex-1 space-y-3">
            <div className="h-6 bg-gray-200 rounded w-1/3 animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded w-1/4 animate-pulse"></div>
          </div>
        </div>
        <div className="space-y-2">
          <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6 animate-pulse"></div>
        </div>
      </div>
    );
  }

  if (!principal) {
    return null;
  }

  return (
    <div data-testid="principal-message" className="bg-white rounded-lg shadow-lg p-8">
      <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-6">
        {principal.photo_url && (
          <Image
            src={principal.photo_url}
            alt={principal.principal_name}
            width={120}
            height={120}
            className="rounded-full object-cover"
          />
        )}

        <div className="flex-1 text-center md:text-left">
          <h2 data-testid="principal-name" className="text-2xl font-bold text-gray-800 mb-1">
            {principal.principal_name}
          </h2>
          {principal.qualification && (
            <p className="text-gray-600 mb-4">{principal.qualification}</p>
          )}

          <div className="text-gray-700 whitespace-pre-wrap leading-relaxed">
            {principal.message}
          </div>

          {(principal.email || principal.phone) && (
            <div className="mt-4 space-y-1 text-sm text-gray-600">
              {principal.email && (
                <p>
                  <span className="font-semibold">Email:</span>{' '}
                  <a href={`mailto:${principal.email}`} className="text-blue-600 hover:underline">
                    {principal.email}
                  </a>
                </p>
              )}
              {principal.phone && (
                <p>
                  <span className="font-semibold">Phone:</span> {principal.phone}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
