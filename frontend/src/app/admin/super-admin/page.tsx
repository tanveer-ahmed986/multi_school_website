/**
 * Super admin dashboard - School management.
 * (T172 - Implementation)
 */
'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { schoolService } from '../../../services/schoolService';

interface School {
  school_id: string;
  school_name: string;
  subdomain: string;
  contact_email: string;
  is_active: boolean;
  storage_used_bytes: number;
  storage_limit_bytes: number;
}

export default function SuperAdminDashboard() {
  const [schools, setSchools] = useState<School[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchSchools();
  }, []);

  const fetchSchools = async () => {
    try {
      const data = await schoolService.listSchools({ search: searchTerm || undefined });
      setSchools(data);
    } catch (error) {
      console.error('Failed to fetch schools:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold text-gray-800">Super Admin Dashboard</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <div className="flex-1 mr-4">
            <input
              type="text"
              placeholder="Search schools..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && fetchSchools()}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <Link
            href="/admin/super-admin/create"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg whitespace-nowrap"
          >
            + Create School
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading schools...</div>
        ) : schools.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No schools found. Create your first school to get started.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {schools.map((school) => (
              <div key={school.school_id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold text-gray-800">{school.school_name}</h3>
                  <span
                    className={`px-2 py-1 rounded text-xs font-semibold ${
                      school.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {school.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>

                <div className="space-y-2 text-sm text-gray-600 mb-4">
                  <p>
                    <span className="font-semibold">Subdomain:</span> {school.subdomain}.domain.com
                  </p>
                  <p>
                    <span className="font-semibold">Email:</span> {school.contact_email}
                  </p>
                  <p>
                    <span className="font-semibold">Storage:</span>{' '}
                    {formatBytes(school.storage_used_bytes)} / {formatBytes(school.storage_limit_bytes)}
                  </p>
                </div>

                <div className="flex space-x-2">
                  <Link
                    href={`/admin/super-admin/schools/${school.school_id}`}
                    className="flex-1 text-center bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm"
                  >
                    View
                  </Link>
                  <a
                    href={`http://${school.subdomain}.localhost:3000`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 text-center bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-sm"
                  >
                    Visit
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
