/**
 * Top Students Component - Display top performing students on homepage
 */
'use client';

import React, { useEffect, useState } from 'react';

interface StudentResult {
  roll_no: string;
  name: string;
  marks: Record<string, number>;
  total: number;
  percentage: number;
  grade: string;
  rank: number;
}

interface ResultWithStudents {
  result_id: string;
  academic_year: string;
  class_level: string;
  exam_type: string;
  students: StudentResult[];
}

export function TopStudents() {
  const [topStudents, setTopStudents] = useState<StudentResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [examInfo, setExamInfo] = useState({ class: '', exam: '' });

  useEffect(() => {
    fetchTopStudents();
  }, []);

  const fetchTopStudents = async () => {
    try {
      // Fetch the latest result (Class 10 Mid-Term as default)
      const response = await fetch('http://localhost:8000/public/results/1/students');
      const data: ResultWithStudents = await response.json();

      console.log('Fetched data:', data);
      console.log('Students count:', data.students?.length);

      if (data.students && data.students.length > 0) {
        // Get top 3 students by rank
        const top3 = data.students
          .sort((a, b) => a.rank - b.rank)
          .slice(0, 3);

        console.log('Top 3 students:', top3);

        setTopStudents(top3);
        setExamInfo({
          class: data.class_level,
          exam: data.exam_type
        });
      } else {
        console.log('No students found in data');
      }
    } catch (error) {
      console.error('Failed to fetch top students:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (topStudents.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">🏆 Top Performers</h3>
        <p className="text-gray-500">No results available yet.</p>
      </div>
    );
  }

  const getRankBadgeColor = (rank: number) => {
    switch (rank) {
      case 1:
        return 'bg-gradient-to-r from-yellow-400 to-yellow-600 text-white';
      case 2:
        return 'bg-gradient-to-r from-gray-300 to-gray-500 text-gray-800';
      case 3:
        return 'bg-gradient-to-r from-orange-400 to-orange-600 text-white';
      default:
        return 'bg-blue-500 text-white';
    }
  };

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return '🏅';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-4">
        <h3 className="text-xl font-bold text-gray-800 mb-1">🏆 Top Performers</h3>
        <p className="text-sm text-gray-500">
          {examInfo.class} - {examInfo.exam}
        </p>
      </div>

      <div className="space-y-3">
        {topStudents.map((student) => (
          <div
            key={student.roll_no}
            className={`relative p-4 rounded-lg border-2 transition-all hover:shadow-md ${
              student.rank === 1
                ? 'border-yellow-400 bg-yellow-50'
                : student.rank === 2
                ? 'border-gray-400 bg-gray-50'
                : 'border-orange-400 bg-orange-50'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-2xl">{getRankIcon(student.rank)}</span>
                  <div>
                    <h4 className="font-bold text-gray-800">{student.name}</h4>
                    <p className="text-xs text-gray-500">Roll No: {student.roll_no}</p>
                  </div>
                </div>

                <div className="mt-2 flex gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Score:</span>
                    <span className="font-semibold text-gray-800 ml-1">
                      {student.total}/{Object.keys(student.marks).length * 100}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Percentage:</span>
                    <span className="font-semibold text-green-600 ml-1">
                      {student.percentage.toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex flex-col items-end gap-2">
                <span
                  className={`px-3 py-1 rounded-full text-sm font-bold ${getRankBadgeColor(
                    student.rank
                  )}`}
                >
                  Rank #{student.rank}
                </span>
                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-semibold">
                  Grade {student.grade}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <a
          href="/results"
          className="text-blue-600 hover:text-blue-800 font-medium text-sm flex items-center justify-center gap-1 transition-colors"
        >
          View All Results
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </a>
      </div>
    </div>
  );
}
