/**
 * Results page - Display published results with professional showcase.
 * Enhanced with ExamResultsShowcase component
 */
'use client';

import React from 'react';
import { ExamResultsShowcase } from '../../components/public/ExamResultsShowcase';

export default function ResultsPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">📊 Examination Results</h1>
        <p className="text-gray-600">View detailed examination results and student performance</p>
      </div>

      <ExamResultsShowcase />
    </div>
  );
}
