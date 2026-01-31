/**
 * Faculty page - Display all visible faculty members.
 * (T075 - Implementation)
 */
'use client';

import React, { useEffect, useState } from 'react';
import { publicService } from '../../services/publicService';
import { FacultyCard } from '../../components/public/FacultyCard';
import type { Faculty } from '../../types/Faculty';

export default function FacultyPage() {
  const [faculty, setFaculty] = useState<Faculty[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFaculty = async () => {
      try {
        const data = await publicService.getFaculty();
        setFaculty(data);
      } catch (error) {
        console.error('Failed to fetch faculty:', error);
        setFaculty([]);
      } finally {
        setLoading(false);
      }
    };

    fetchFaculty();
  }, []);

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Our Faculty</h1>

      {loading ? (
        <div data-testid="faculty-grid" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="h-64 bg-gray-200 animate-pulse"></div>
              <div className="p-6 space-y-3">
                <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3 animate-pulse"></div>
                <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
              </div>
            </div>
          ))}
        </div>
      ) : faculty.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No faculty members available at this time.
        </div>
      ) : (
        <div data-testid="faculty-grid" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {faculty.map((member) => (
            <FacultyCard key={member.faculty_id} faculty={member} />
          ))}
        </div>
      )}
    </div>
  );
}
