/**
 * Simple Top Students Component - For debugging
 */
'use client';

import React, { useEffect, useState } from 'react';

export function TopStudentsSimple() {
  const [students, setStudents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetch('/data/results.json')
      .then(res => res.json())
      .then(data => {
        console.log('===== API Response =====', data);

        if (data && data.length > 0 && data[0].students) {
          const top3 = data[0].students.slice(0, 3).sort((a: any, b: any) => a.rank - b.rank);
          console.log('===== Top 3 Students =====', top3);
          setStudents(top3);
        } else {
          setError('No students data in response');
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('===== ERROR =====', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="bg-yellow-100 border-2 border-yellow-500 p-6 rounded-lg">
        <h3 className="text-xl font-bold">Loading top students...</h3>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border-2 border-red-500 p-6 rounded-lg">
        <h3 className="text-xl font-bold text-red-800">Error: {error}</h3>
      </div>
    );
  }

  if (students.length === 0) {
    return (
      <div className="bg-blue-100 border-2 border-blue-500 p-6 rounded-lg">
        <h3 className="text-xl font-bold text-blue-800">No students found</h3>
        <p className="text-sm">Students array is empty</p>
      </div>
    );
  }

  return (
    <div className="bg-green-100 border-4 border-green-500 p-6 rounded-lg">
      <h2 className="text-2xl font-bold mb-4 text-green-800">
        🏆 TOP 3 STUDENTS (Showing {students.length})
      </h2>

      {students.map((student, index) => (
        <div
          key={student.roll_no || index}
          className="bg-white p-4 mb-3 rounded-lg border-2 border-gray-300"
        >
          <div className="text-lg font-bold">
            #{student.rank} - {student.name}
          </div>
          <div className="text-sm text-gray-600">
            Roll: {student.roll_no} | Grade: {student.grade} | {student.percentage}%
          </div>
          <div className="text-xs text-gray-500 mt-1">
            Total: {student.total} marks
          </div>
        </div>
      ))}
    </div>
  );
}
