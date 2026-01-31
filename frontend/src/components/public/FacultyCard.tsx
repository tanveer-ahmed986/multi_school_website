/**
 * Faculty card component for displaying individual faculty member.
 * (T089 - Implementation)
 */
'use client';

import React from 'react';
import Image from 'next/image';
import type { Faculty } from '../../types/Faculty';

interface FacultyCardProps {
  faculty: Faculty;
}

export function FacultyCard({ faculty }: FacultyCardProps) {
  return (
    <div data-testid="faculty-card" className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {faculty.photo_url && (
        <div className="relative h-64 bg-gray-200">
          <Image
            src={faculty.photo_url}
            alt={faculty.full_name}
            fill
            className="object-cover"
          />
        </div>
      )}

      <div className="p-6">
        <h3 data-testid="faculty-name" className="text-xl font-bold text-gray-800 mb-1">
          {faculty.full_name}
        </h3>

        <p data-testid="faculty-designation" className="text-blue-600 font-medium mb-2">
          {faculty.designation}
        </p>

        <p data-testid="faculty-qualification" className="text-gray-600 text-sm mb-3">
          {faculty.qualification}
        </p>

        {faculty.subject && (
          <p className="text-gray-700 text-sm mb-2">
            <span className="font-semibold">Subject:</span> {faculty.subject}
          </p>
        )}

        <p className="text-gray-700 text-sm mb-3">
          <span className="font-semibold">Experience:</span> {faculty.experience_years} years
        </p>

        {faculty.bio && (
          <p className="text-gray-600 text-sm mt-3 border-t pt-3">
            {faculty.bio}
          </p>
        )}

        {(faculty.email || faculty.phone) && (
          <div className="mt-4 space-y-1 text-sm text-gray-600 border-t pt-3">
            {faculty.email && (
              <p>
                <a href={`mailto:${faculty.email}`} className="text-blue-600 hover:underline">
                  {faculty.email}
                </a>
              </p>
            )}
            {faculty.phone && (
              <p>{faculty.phone}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
