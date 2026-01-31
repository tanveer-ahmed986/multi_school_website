/**
 * Results table component for displaying student results.
 * (T088 - Implementation)
 */
'use client';

import React, { useState } from 'react';
import type { Result } from '../../types/Result';

interface ResultsTableProps {
  result: Result;
}

export function ResultsTable({ result }: ResultsTableProps) {
  const [sortBy, setSortBy] = useState<'roll' | 'name' | 'marks' | 'percentage'>('roll');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  const sortedStudents = [...result.result_data.students].sort((a, b) => {
    let comparison = 0;

    switch (sortBy) {
      case 'roll':
        comparison = a.roll_number.localeCompare(b.roll_number);
        break;
      case 'name':
        comparison = a.student_name.localeCompare(b.student_name);
        break;
      case 'marks':
        comparison = a.total_marks - b.total_marks;
        break;
      case 'percentage':
        comparison = a.percentage - b.percentage;
        break;
    }

    return sortOrder === 'asc' ? comparison : -comparison;
  });

  const handleSort = (column: typeof sortBy) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  return (
    <div data-testid="results-table" className="overflow-x-auto">
      {/* Statistics Section */}
      <div data-testid="result-statistics" className="bg-blue-50 p-6 rounded-lg mb-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Statistics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">
              {result.result_data.statistics.total_students}
            </p>
            <p className="text-sm text-gray-600">Total Students</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">
              {result.result_data.statistics.pass_percentage}%
            </p>
            <p className="text-sm text-gray-600">Pass Percentage</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-purple-600">
              {result.result_data.statistics.highest_marks}
            </p>
            <p className="text-sm text-gray-600">Highest Marks</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-orange-600">
              {result.result_data.statistics.average_percentage}%
            </p>
            <p className="text-sm text-gray-600">Average</p>
          </div>
        </div>
      </div>

      {/* Results Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('roll')}
              >
                Roll No {sortBy === 'roll' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('name')}
              >
                Name {sortBy === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('marks')}
              >
                Total Marks {sortBy === 'marks' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('percentage')}
              >
                Percentage {sortBy === 'percentage' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Grade
              </th>
              {sortedStudents[0]?.rank && (
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rank
                </th>
              )}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedStudents.map((student) => (
              <tr key={student.roll_number} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {student.roll_number}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                  {student.student_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                  {student.total_marks}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                  {student.percentage.toFixed(2)}%
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    student.grade === 'A+' ? 'bg-green-100 text-green-800' :
                    student.grade === 'A' ? 'bg-blue-100 text-blue-800' :
                    student.grade === 'B' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {student.grade}
                  </span>
                </td>
                {student.rank && (
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {student.rank}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
