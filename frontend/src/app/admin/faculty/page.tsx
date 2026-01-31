/**
 * Faculty management page.
 * (T144 - Implementation)
 * (T194 - Permission guard added)
 */
'use client';

import React from 'react';
import { FacultyManager } from '../../../components/admin/FacultyManager';
import { PermissionGuard } from '../../../components/guards/PermissionGuard';

export default function FacultyManagementPage() {
  return (
    <PermissionGuard permission="canAccessFaculty">
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          <FacultyManager />
        </div>
      </div>
    </PermissionGuard>
  );
}
