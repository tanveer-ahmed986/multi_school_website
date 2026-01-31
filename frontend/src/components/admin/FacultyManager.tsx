/**
 * Faculty management component with CRUD operations.
 * (T143 - Implementation)
 */
'use client';

import React, { useState, useEffect } from 'react';
import { contentService } from '../../services/contentService';
import type { Faculty } from '../../types/Faculty';

export function FacultyManager() {
  const [faculty, setFaculty] = useState<Faculty[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    full_name: '',
    designation: '',
    qualification: '',
    experience_years: 0,
    subject: '',
    email: '',
    phone: '',
    bio: '',
  });

  useEffect(() => {
    fetchFaculty();
  }, []);

  const fetchFaculty = async () => {
    try {
      const data = await contentService.listFaculty(true);
      setFaculty(data);
    } catch (error) {
      console.error('Failed to fetch faculty:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (editingId) {
        await contentService.updateFaculty(editingId, formData);
      } else {
        await contentService.createFaculty(formData);
      }

      await fetchFaculty();
      resetForm();
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Operation failed'}`);
    }
  };

  const handleEdit = (member: Faculty) => {
    setEditingId(member.faculty_id);
    setFormData({
      full_name: member.full_name,
      designation: member.designation,
      qualification: member.qualification,
      experience_years: member.experience_years,
      subject: member.subject || '',
      email: member.email || '',
      phone: member.phone || '',
      bio: member.bio || '',
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this faculty member?')) return;

    try {
      await contentService.deleteFaculty(id);
      await fetchFaculty();
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Delete failed'}`);
    }
  };

  const resetForm = () => {
    setFormData({
      full_name: '',
      designation: '',
      qualification: '',
      experience_years: 0,
      subject: '',
      email: '',
      phone: '',
      bio: '',
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) {
    return <div className="text-center py-8">Loading faculty...</div>;
  }

  return (
    <div>
      <div className="mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Faculty Management</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          {showForm ? 'Cancel' : 'Add Faculty'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h3 className="text-lg font-bold mb-4">
            {editingId ? 'Edit Faculty Member' : 'Add New Faculty Member'}
          </h3>

          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name *
              </label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Designation *
              </label>
              <input
                type="text"
                value={formData.designation}
                onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Qualification *
              </label>
              <input
                type="text"
                value={formData.qualification}
                onChange={(e) => setFormData({ ...formData, qualification: e.target.value })}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Experience (Years) *
              </label>
              <input
                type="number"
                value={formData.experience_years}
                onChange={(e) => setFormData({ ...formData, experience_years: parseInt(e.target.value) })}
                required
                min="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Subject
              </label>
              <input
                type="text"
                value={formData.subject}
                onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Phone
              </label>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bio
              </label>
              <textarea
                value={formData.bio}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>

            <div className="md:col-span-2 flex space-x-4">
              <button
                type="submit"
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg"
              >
                {editingId ? 'Update' : 'Add'} Faculty
              </button>
              <button
                type="button"
                onClick={resetForm}
                className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {faculty.map((member) => (
          <div key={member.faculty_id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold text-gray-800 mb-1">{member.full_name}</h3>
            <p className="text-blue-600 font-medium mb-2">{member.designation}</p>
            <p className="text-gray-600 text-sm mb-2">{member.qualification}</p>
            <p className="text-gray-600 text-sm mb-4">Experience: {member.experience_years} years</p>

            {member.subject && (
              <p className="text-gray-600 text-sm mb-2">Subject: {member.subject}</p>
            )}

            <div className="flex space-x-2 mt-4">
              <button
                onClick={() => handleEdit(member)}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(member.faculty_id)}
                className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 rounded-lg text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {faculty.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No faculty members added yet. Click "Add Faculty" to get started.
        </div>
      )}
    </div>
  );
}
