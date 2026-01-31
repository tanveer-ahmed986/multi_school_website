/**
 * Results management page.
 * (T147 - Implementation)
 * (T194 - Permission guard added)
 */
'use client';

import React, { useState } from 'react';
import { contentService } from '../../../services/contentService';
import { PermissionGuard } from '../../../components/guards/PermissionGuard';

export default function ResultsManagementPage() {
  const [formData, setFormData] = useState({
    academic_year: '',
    class_level: '',
    exam_type: '',
    is_published: false,
  });
  const [resultData, setResultData] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const parsedData = JSON.parse(resultData);
      await contentService.createResult({
        ...formData,
        result_data: parsedData,
      });
      alert('Result uploaded successfully!');
      setResultData('');
    } catch (error: any) {
      alert(`Error: ${error.message || 'Upload failed'}`);
    }
  };

  return (
    <PermissionGuard permission="canAccessResults">
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold text-gray-800 mb-8">Results Management</h1>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4">Upload New Result</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Academic Year
                </label>
                <input
                  type="text"
                  value={formData.academic_year}
                  onChange={(e) => setFormData({ ...formData, academic_year: e.target.value })}
                  placeholder="2024-25"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Class Level
                </label>
                <input
                  type="text"
                  value={formData.class_level}
                  onChange={(e) => setFormData({ ...formData, class_level: e.target.value })}
                  placeholder="Class 10"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Exam Type
                </label>
                <input
                  type="text"
                  value={formData.exam_type}
                  onChange={(e) => setFormData({ ...formData, exam_type: e.target.value })}
                  placeholder="Annual"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Result Data (JSON)
              </label>
              <textarea
                value={resultData}
                onChange={(e) => setResultData(e.target.value)}
                placeholder={'{\n  "students": [...],\n  "statistics": {...}\n}'}
                required
                rows={10}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_published"
                checked={formData.is_published}
                onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                className="mr-2"
              />
              <label htmlFor="is_published" className="text-sm text-gray-700">
                Publish immediately
              </label>
            </div>

            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
            >
              Upload Result
            </button>
          </form>
        </div>
      </div>
    </PermissionGuard>
  );
}
