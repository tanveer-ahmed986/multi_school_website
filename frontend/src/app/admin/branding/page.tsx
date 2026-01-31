/**
 * Branding settings page for school administrators.
 * (T179 - Implementation)
 *
 * Allows customization of:
 * - School logo
 * - Primary and secondary theme colors
 * - Contact information (email, phone, address)
 */
'use client';

import React, { useState, useEffect } from 'react';
import { contentService } from '../../../services/contentService';
import { publicService } from '../../../services/publicService';
import { ColorPreview } from '../../../components/admin/ColorPreview';

interface BrandingData {
  logo_url: string;
  primary_color: string;
  secondary_color: string;
  contact_email: string;
  contact_phone: string;
  address: string;
}

export default function BrandingManagementPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const [formData, setFormData] = useState<BrandingData>({
    logo_url: '',
    primary_color: '#0A3D62',
    secondary_color: '#EAF2F8',
    contact_email: '',
    contact_phone: '',
    address: '',
  });

  // Load current branding settings
  useEffect(() => {
    const loadBranding = async () => {
      try {
        const schoolInfo = await publicService.getSchoolInfo();
        setFormData({
          logo_url: schoolInfo.logo_url || '',
          primary_color: schoolInfo.primary_color || '#0A3D62',
          secondary_color: schoolInfo.secondary_color || '#EAF2F8',
          contact_email: schoolInfo.contact_email || '',
          contact_phone: schoolInfo.contact_phone || '',
          address: schoolInfo.address || '',
        });
      } catch (err: any) {
        setError('Failed to load branding settings');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadBranding();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    setError('');

    try {
      // Validate hex colors
      const hexColorRegex = /^#[0-9A-Fa-f]{6}$/;
      if (!hexColorRegex.test(formData.primary_color)) {
        throw new Error('Primary color must be a valid hex code (e.g., #FF5733)');
      }
      if (!hexColorRegex.test(formData.secondary_color)) {
        throw new Error('Secondary color must be a valid hex code (e.g., #C70039)');
      }

      // Validate email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (formData.contact_email && !emailRegex.test(formData.contact_email)) {
        throw new Error('Please enter a valid email address');
      }

      await contentService.updateBranding(formData);
      setMessage('Branding updated successfully!');

      // Reload the page after 1.5 seconds to show updated branding
      setTimeout(() => {
        window.location.reload();
      }, 1500);
    } catch (err: any) {
      setError(err.message || err.response?.data?.detail || 'Failed to update branding');
    } finally {
      setSaving(false);
    }
  };

  const handleLogoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file');
      return;
    }

    // Validate file size (max 2MB)
    if (file.size > 2 * 1024 * 1024) {
      setError('Logo file size must be less than 2MB');
      return;
    }

    // TODO: In production, upload to file storage service
    // For now, we'll just show a placeholder message
    setMessage('Logo upload feature will be integrated with file storage service');

    // Mock URL for demonstration
    // In production, this would be the URL returned from file upload service
    // const uploadedUrl = await fileStorageService.uploadFile(file);
    // setFormData({ ...formData, logo_url: uploadedUrl });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          <div className="text-center py-12">Loading branding settings...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Branding Settings</h1>

        {/* Messages */}
        {message && (
          <div className="mb-6 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            {message}
          </div>
        )}
        {error && (
          <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Form */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 space-y-6">
              {/* Logo Upload Section */}
              <div>
                <h2 className="text-xl font-bold mb-4">School Logo</h2>
                <div className="space-y-3">
                  {formData.logo_url && (
                    <div className="mb-3">
                      <img
                        src={formData.logo_url}
                        alt="Current school logo"
                        className="h-20 object-contain"
                      />
                    </div>
                  )}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Upload New Logo
                    </label>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleLogoUpload}
                      className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    />
                    <p className="text-sm text-gray-500 mt-1">
                      Recommended: PNG or JPG, max 2MB
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Or enter logo URL
                    </label>
                    <input
                      type="url"
                      name="logo_url"
                      value={formData.logo_url}
                      onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="https://example.com/logo.png"
                    />
                  </div>
                </div>
              </div>

              <hr />

              {/* Theme Colors Section */}
              <div>
                <h2 className="text-xl font-bold mb-4">Theme Colors</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Primary Color
                    </label>
                    <div className="flex items-center space-x-3">
                      <input
                        type="color"
                        name="primary_color"
                        value={formData.primary_color}
                        onChange={(e) => setFormData({ ...formData, primary_color: e.target.value })}
                        className="h-12 w-20 border border-gray-300 rounded cursor-pointer"
                      />
                      <input
                        type="text"
                        value={formData.primary_color}
                        onChange={(e) => setFormData({ ...formData, primary_color: e.target.value })}
                        pattern="^#[0-9A-Fa-f]{6}$"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg font-mono"
                        placeholder="#0A3D62"
                      />
                    </div>
                    <p className="text-sm text-gray-500 mt-1">Used for headers, buttons</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Secondary Color
                    </label>
                    <div className="flex items-center space-x-3">
                      <input
                        type="color"
                        name="secondary_color"
                        value={formData.secondary_color}
                        onChange={(e) => setFormData({ ...formData, secondary_color: e.target.value })}
                        className="h-12 w-20 border border-gray-300 rounded cursor-pointer"
                      />
                      <input
                        type="text"
                        value={formData.secondary_color}
                        onChange={(e) => setFormData({ ...formData, secondary_color: e.target.value })}
                        pattern="^#[0-9A-Fa-f]{6}$"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg font-mono"
                        placeholder="#EAF2F8"
                      />
                    </div>
                    <p className="text-sm text-gray-500 mt-1">Used for backgrounds, accents</p>
                  </div>
                </div>
              </div>

              <hr />

              {/* Contact Information Section */}
              <div>
                <h2 className="text-xl font-bold mb-4">Contact Information</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Contact Email *
                    </label>
                    <input
                      type="email"
                      name="contact_email"
                      value={formData.contact_email}
                      onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="admin@school.edu"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Contact Phone
                    </label>
                    <input
                      type="tel"
                      name="contact_phone"
                      value={formData.contact_phone}
                      onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="+1-555-0100"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Address
                    </label>
                    <textarea
                      name="address"
                      value={formData.address}
                      onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      placeholder="123 School St, City, State 12345"
                    />
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => window.history.back()}
                  className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium disabled:bg-blue-300"
                >
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </div>

          {/* Live Preview Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 sticky top-8">
              <ColorPreview
                primaryColor={formData.primary_color}
                secondaryColor={formData.secondary_color}
                logoUrl={formData.logo_url || undefined}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
