/**
 * Notice board component displaying active notices with priority badges.
 * (T086 - Implementation)
 */
'use client';

import React, { useEffect, useState } from 'react';
import { publicService } from '../../services/publicService';
import type { Notice } from '../../types/Notice';
import { PRIORITY_LABELS, PRIORITY_COLORS } from '../../types/Notice';

interface NoticeBoardProps {
  limit?: number; // Limit number of notices to display (for homepage)
}

export function NoticeBoard({ limit }: NoticeBoardProps) {
  const [notices, setNotices] = useState<Notice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNotices = async () => {
      try {
        const response = await fetch('/data/notices.json');
        const rawData = await response.json();

        // Map static data to Notice type
        const mappedData = rawData
          .filter((item: any) => item.is_active)
          .map((item: any) => ({
            notice_id: item.id,
            title: item.title,
            description: item.content,
            priority_level: item.priority === 'high' ? 3 : item.priority === 'medium' ? 2 : 1,
            category: '',
            published_date: item.published_date,
            expiry_date: null,
            attachment_url: null
          }));

        setNotices(limit ? mappedData.slice(0, limit) : mappedData);
      } catch (error) {
        console.error('Failed to fetch notices:', error);
        setNotices([]);
      } finally {
        setLoading(false);
      }
    };

    fetchNotices();
  }, [limit]);

  if (loading) {
    return (
      <div data-testid="notice-board" className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white p-6 rounded-lg shadow animate-pulse">
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-3"></div>
            <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        ))}
      </div>
    );
  }

  if (notices.length === 0) {
    return (
      <div data-testid="notice-board" className="text-center py-8 text-gray-500">
        No active notices at this time.
      </div>
    );
  }

  return (
    <div data-testid="notice-board" className="space-y-4">
      {notices.map((notice) => (
        <div
          key={notice.notice_id}
          data-testid="notice-card"
          className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between mb-2">
            <h3 data-testid="notice-title" className="text-xl font-bold text-gray-800 flex-1">
              {notice.title}
            </h3>
            <span
              data-testid="priority-badge"
              className={`px-3 py-1 rounded-full text-xs font-semibold ${
                PRIORITY_COLORS[notice.priority_level as keyof typeof PRIORITY_COLORS]
              }`}
            >
              {PRIORITY_LABELS[notice.priority_level as keyof typeof PRIORITY_LABELS]}
            </span>
          </div>

          <p data-testid="notice-description" className="text-gray-600 mb-3 whitespace-pre-wrap">
            {notice.description}
          </p>

          <div className="flex items-center justify-between text-sm text-gray-500">
            <span data-testid="notice-date">
              {new Date(notice.published_date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </span>

            {notice.category && (
              <span className="px-2 py-1 bg-gray-100 rounded text-gray-700">
                {notice.category}
              </span>
            )}
          </div>

          {notice.attachment_url && (
            <a
              data-testid="attachment-link"
              href={notice.attachment_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-3 text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              📎 View Attachment
            </a>
          )}
        </div>
      ))}
    </div>
  );
}
