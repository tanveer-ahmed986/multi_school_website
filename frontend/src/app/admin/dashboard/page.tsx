/**
 * Admin dashboard - Content management overview.
 * (T141 - Implementation)
 */
'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '../../../hooks/useAuth';

export default function AdminDashboard() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/admin/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  const quickActions = [
    {
      title: 'Faculty Management',
      description: 'Add, edit, or remove faculty members',
      href: '/admin/faculty',
      icon: '👨‍🏫',
      color: 'bg-blue-600',
    },
    {
      title: 'Results Upload',
      description: 'Upload and publish student results',
      href: '/admin/results',
      icon: '📊',
      color: 'bg-green-600',
    },
    {
      title: 'Notices',
      description: 'Create and manage announcements',
      href: '/admin/notices',
      icon: '📢',
      color: 'bg-orange-600',
    },
    {
      title: 'Gallery',
      description: 'Upload and organize photos',
      href: '/admin/gallery',
      icon: '🖼️',
      color: 'bg-purple-600',
    },
    {
      title: 'Principal Profile',
      description: "Update principal's message and photo",
      href: '/admin/principal',
      icon: '👔',
      color: 'bg-indigo-600',
    },
    {
      title: 'Branding',
      description: 'Customize school colors and logo',
      href: '/admin/branding',
      icon: '🎨',
      color: 'bg-pink-600',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">{user.full_name}</span>
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Welcome, {user.full_name}!
          </h2>
          <p className="text-gray-600">
            Role: <span className="font-medium">{user.role}</span>
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {quickActions.map((action) => (
            <Link
              key={action.href}
              href={action.href}
              className="block bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
            >
              <div className="flex items-center mb-4">
                <div className={`${action.color} text-white text-3xl w-14 h-14 rounded-lg flex items-center justify-center mr-4`}>
                  {action.icon}
                </div>
                <h3 className="text-lg font-bold text-gray-800">{action.title}</h3>
              </div>
              <p className="text-gray-600 text-sm">{action.description}</p>
            </Link>
          ))}
        </div>

        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Quick Stats</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">--</div>
              <div className="text-sm text-gray-600">Faculty Members</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">--</div>
              <div className="text-sm text-gray-600">Published Results</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600">--</div>
              <div className="text-sm text-gray-600">Active Notices</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">--</div>
              <div className="text-sm text-gray-600">Gallery Images</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
