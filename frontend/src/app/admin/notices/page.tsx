/**
 * Notices management page.
 * (T150 - Implementation)
 */
'use client';

import React, { useState } from 'react';
import { contentService } from '../../../services/contentService';

export default function NoticesManagementPage() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority_level: 1,
    category: 'general',
    expiry_date: '',
    is_published: false,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await contentService.createNotice({
        ...formData,
        expiry_date: formData.expiry_date || null,
      });
      alert('Notice created successfully!');
      setFormData({
        title: '',
        description: '',
        priority_level: 1,
        category: 'general',
        expiry_date: '',
        is_published: false,
      });
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Create failed'}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Notices Management</h1>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4">Create New Notice</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                required
                rows={5}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Priority Level
                </label>
                <select
                  value={formData.priority_level}
                  onChange={(e) => setFormData({ ...formData, priority_level: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  <option value={0}>Low</option>
                  <option value={1}>Normal</option>
                  <option value={2}>Important</option>
                  <option value={3}>High</option>
                  <option value={4}>Very High</option>
                  <option value={5}>Urgent</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="general">General</option>
                  <option value="academic">Academic</option>
                  <option value="events">Events</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Expiry Date
                </label>
                <input
                  type="datetime-local"
                  value={formData.expiry_date}
                  onChange={(e) => setFormData({ ...formData, expiry_date: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
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
              Create Notice
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
