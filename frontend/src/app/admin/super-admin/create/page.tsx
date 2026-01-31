/**
 * Create new school form (Super Admin).
 * (T173 - Implementation)
 */
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { schoolService } from '../../../../services/schoolService';

export default function CreateSchoolPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [schoolId, setSchoolId] = useState('');

  const [schoolData, setSchoolData] = useState({
    school_name: '',
    subdomain: '',
    contact_email: '',
    contact_phone: '',
    address: '',
    primary_color: '#0A3D62',
    secondary_color: '#EAF2F8',
  });

  const [adminData, setAdminData] = useState({
    email: '',
    password: '',
    full_name: '',
  });

  const handleSchoolSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const school = await schoolService.createSchool(schoolData);
      setSchoolId(school.school_id);
      setStep(2);
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to create school'}`);
    }
  };

  const handleAdminSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await schoolService.assignAdmin(schoolId, adminData);
      alert('School created and admin assigned successfully!');
      router.push('/admin/super-admin');
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to assign admin'}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4 max-w-2xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Create New School</h1>

        {/* Progress Indicator */}
        <div className="mb-8 flex items-center">
          <div className={`flex-1 h-2 rounded ${step >= 1 ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
          <div className="px-4 text-sm font-medium text-gray-600">School Info</div>
          <div className={`flex-1 h-2 rounded ${step >= 2 ? 'bg-blue-600' : 'bg-gray-300'}`}></div>
          <div className="px-4 text-sm font-medium text-gray-600">Admin Assignment</div>
        </div>

        {step === 1 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Step 1: School Information</h2>

            <form onSubmit={handleSchoolSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  School Name *
                </label>
                <input
                  type="text"
                  value={schoolData.school_name}
                  onChange={(e) => setSchoolData({ ...schoolData, school_name: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  placeholder="Springfield High School"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Subdomain * (lowercase, alphanumeric, hyphens only)
                </label>
                <div className="flex items-center">
                  <input
                    type="text"
                    value={schoolData.subdomain}
                    onChange={(e) => setSchoolData({ ...schoolData, subdomain: e.target.value.toLowerCase() })}
                    required
                    pattern="[a-z0-9-]{3,50}"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-l-lg"
                    placeholder="springfield"
                  />
                  <span className="px-3 py-2 bg-gray-100 border border-l-0 border-gray-300 rounded-r-lg text-gray-600">
                    .domain.com
                  </span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contact Email *
                </label>
                <input
                  type="email"
                  value={schoolData.contact_email}
                  onChange={(e) => setSchoolData({ ...schoolData, contact_email: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contact Phone
                </label>
                <input
                  type="tel"
                  value={schoolData.contact_phone}
                  onChange={(e) => setSchoolData({ ...schoolData, contact_phone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Address
                </label>
                <textarea
                  value={schoolData.address}
                  onChange={(e) => setSchoolData({ ...schoolData, address: e.target.value })}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Primary Color
                  </label>
                  <input
                    type="color"
                    value={schoolData.primary_color}
                    onChange={(e) => setSchoolData({ ...schoolData, primary_color: e.target.value })}
                    className="w-full h-10 border border-gray-300 rounded-lg"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Secondary Color
                  </label>
                  <input
                    type="color"
                    value={schoolData.secondary_color}
                    onChange={(e) => setSchoolData({ ...schoolData, secondary_color: e.target.value })}
                    className="w-full h-10 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
              >
                Next: Assign Admin
              </button>
            </form>
          </div>
        )}

        {step === 2 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Step 2: Assign School Administrator</h2>

            <form onSubmit={handleAdminSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Admin Full Name *
                </label>
                <input
                  type="text"
                  value={adminData.full_name}
                  onChange={(e) => setAdminData({ ...adminData, full_name: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Admin Email *
                </label>
                <input
                  type="email"
                  value={adminData.email}
                  onChange={(e) => setAdminData({ ...adminData, email: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Admin Password *
                </label>
                <input
                  type="password"
                  value={adminData.password}
                  onChange={(e) => setAdminData({ ...adminData, password: e.target.value })}
                  required
                  minLength={8}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
                <p className="text-sm text-gray-500 mt-1">Minimum 8 characters</p>
              </div>

              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium"
                >
                  Back
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium"
                >
                  Create School
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
