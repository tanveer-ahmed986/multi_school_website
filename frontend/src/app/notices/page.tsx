/**
 * Notices page - Display all active notices.
 * (T078 - Implementation)
 */
'use client';

import React from 'react';
import { NoticeBoard } from '../../components/public/NoticeBoard';

export default function NoticesPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Notices & Announcements</h1>

      <NoticeBoard />
    </div>
  );
}
