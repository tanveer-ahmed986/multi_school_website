/**
 * Exam Results Showcase Component - Professional results display for client demo
 */
'use client';

import React, { useEffect, useState } from 'react';

interface Student {
  roll_no: string;
  name: string;
  marks: Record<string, number>;
  total: number;
  percentage: number;
  grade: string;
  rank: number;
}

interface ExamResult {
  id: string;
  academic_year: string;
  class_level: string;
  exam_type: string;
  total_students: number;
  pass_percentage: number;
  average_marks: number;
}

export function ExamResultsShowcase() {
  const [results, setResults] = useState<ExamResult[]>([]);
  const [selectedResult, setSelectedResult] = useState<string | null>(null);
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const modalContentRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchResults();
  }, []);

  // Auto-focus modal content when opened
  useEffect(() => {
    if (selectedResult && modalContentRef.current) {
      modalContentRef.current.focus();
    }
  }, [selectedResult]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!selectedResult) return;

      const currentIdx = results.findIndex(r => r.id === selectedResult);

      // ESC key closes modal
      if (e.key === 'Escape') {
        setSelectedResult(null);
        return;
      }

      // Left arrow: Navigate to previous result
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        const prevIdx = currentIdx > 0 ? currentIdx - 1 : results.length - 1;
        fetchStudentResults(results[prevIdx].id);
        return;
      }

      // Right arrow: Navigate to next result
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        const nextIdx = currentIdx < results.length - 1 ? currentIdx + 1 : 0;
        fetchStudentResults(results[nextIdx].id);
        return;
      }

      // Up arrow: Scroll up
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (modalContentRef.current) {
          modalContentRef.current.scrollBy({ top: -100, behavior: 'smooth' });
        }
        return;
      }

      // Down arrow: Scroll down
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (modalContentRef.current) {
          modalContentRef.current.scrollBy({ top: 100, behavior: 'smooth' });
        }
        return;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedResult, results]);

  const fetchResults = async () => {
    try {
      const response = await fetch('http://localhost:8000/public/results');
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error fetching results:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStudentResults = async (resultId: string) => {
    setDetailsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/public/results/${resultId}/students`);
      const data = await response.json();
      if (data.students) {
        setStudents(data.students.sort((a: Student, b: Student) => a.rank - b.rank));
        setSelectedResult(resultId);
      }
    } catch (error) {
      console.error('Error fetching student results:', error);
    } finally {
      setDetailsLoading(false);
    }
  };

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case 'A+': return 'bg-green-100 text-green-800 border-green-300';
      case 'A': return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'B+': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'B': return 'bg-orange-100 text-orange-800 border-orange-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getRankMedal = (rank: number) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '🏅';
    }
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-lg shadow-md p-6 animate-pulse">
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Results Overview Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((result) => (
          <div
            key={result.id}
            onClick={() => fetchStudentResults(result.id)}
            className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer border-2 border-transparent hover:border-blue-500 overflow-hidden group"
          >
            {/* Header with gradient */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-800 p-4 text-white">
              <h3 className="text-xl font-bold mb-1">{result.class_level}</h3>
              <p className="text-sm opacity-90">{result.exam_type}</p>
            </div>

            {/* Content */}
            <div className="p-6">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 text-sm">Academic Year</span>
                  <span className="font-semibold text-gray-800">{result.academic_year}</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-gray-600 text-sm">Total Students</span>
                  <span className="font-semibold text-blue-600">{result.total_students}</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-gray-600 text-sm">Pass Rate</span>
                  <span className="font-semibold text-green-600">{result.pass_percentage}%</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-gray-600 text-sm">Class Average</span>
                  <span className="font-semibold text-purple-600">{result.average_marks.toFixed(1)}%</span>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-gray-200">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors group-hover:bg-blue-700">
                  View Student Results →
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Student Results Modal */}
      {selectedResult && (
        <div
          className="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4 backdrop-blur-sm"
          onClick={() => setSelectedResult(null)}
        >
          <div
            className="bg-white rounded-xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden relative"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Navigation Arrows */}
            {results.length > 1 && (
              <>
                {/* Left Arrow */}
                <button
                  onClick={() => {
                    const currentIdx = results.findIndex(r => r.id === selectedResult);
                    const prevIdx = currentIdx > 0 ? currentIdx - 1 : results.length - 1;
                    fetchStudentResults(results[prevIdx].id);
                  }}
                  className="absolute left-4 top-1/2 -translate-y-1/2 z-10 bg-white hover:bg-gray-100 text-gray-800 rounded-full p-3 shadow-lg transition-all hover:scale-110"
                  aria-label="Previous result"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>

                {/* Right Arrow */}
                <button
                  onClick={() => {
                    const currentIdx = results.findIndex(r => r.id === selectedResult);
                    const nextIdx = currentIdx < results.length - 1 ? currentIdx + 1 : 0;
                    fetchStudentResults(results[nextIdx].id);
                  }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 z-10 bg-white hover:bg-gray-100 text-gray-800 rounded-full p-3 shadow-lg transition-all hover:scale-110"
                  aria-label="Next result"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </>
            )}

            {/* Modal Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold mb-1">Student Results</h2>
                  <p className="text-sm opacity-90">
                    {results.find(r => r.id === selectedResult)?.class_level} - {results.find(r => r.id === selectedResult)?.exam_type}
                  </p>
                  {results.length > 1 && (
                    <p className="text-xs opacity-75 mt-2">
                      ← → Navigate between results • ↑ ↓ Scroll content • ESC Close
                    </p>
                  )}
                </div>
                <button
                  onClick={() => setSelectedResult(null)}
                  className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition-all"
                  aria-label="Close"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Modal Body */}
            <div
              ref={modalContentRef}
              tabIndex={0}
              className="p-6 overflow-y-auto max-h-[calc(90vh-120px)] focus:outline-none"
            >
              {detailsLoading ? (
                <div className="text-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-4 text-gray-600">Loading student results...</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Top 3 Highlight */}
                  {students.slice(0, 3).length > 0 && (
                    <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg p-6 mb-6 border-2 border-yellow-200">
                      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <span className="text-2xl">🏆</span>
                        Top 3 Performers
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {students.slice(0, 3).map((student) => (
                          <div
                            key={student.roll_no}
                            className="bg-white rounded-lg p-4 shadow-md border-2 border-yellow-300"
                          >
                            <div className="text-center mb-2">
                              <span className="text-4xl">{getRankMedal(student.rank)}</span>
                            </div>
                            <h4 className="font-bold text-gray-800 text-center mb-1">{student.name}</h4>
                            <p className="text-sm text-gray-600 text-center mb-2">Roll: {student.roll_no}</p>
                            <div className="flex justify-center gap-3 text-sm">
                              <span className="font-semibold text-green-600">{student.percentage.toFixed(1)}%</span>
                              <span className={`px-2 py-1 rounded-full text-xs font-bold border ${getGradeColor(student.grade)}`}>
                                {student.grade}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* All Students Table */}
                  <div className="bg-white rounded-lg shadow overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Roll No</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Percentage</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Grade</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {students.map((student, index) => (
                          <tr
                            key={student.roll_no}
                            className={`hover:bg-blue-50 transition-colors ${index < 3 ? 'bg-yellow-50' : ''}`}
                          >
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="text-2xl">{getRankMedal(student.rank)}</span>
                              <span className="ml-2 font-semibold text-gray-800">#{student.rank}</span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                              {student.roll_no}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap font-semibold text-gray-800">
                              {student.name}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              <span className="font-semibold">{student.total}</span>
                              <span className="text-gray-500">/{Object.keys(student.marks).length * 100}</span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="text-lg font-bold text-green-600">
                                {student.percentage.toFixed(1)}%
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-3 py-1 rounded-full text-sm font-bold border-2 ${getGradeColor(student.grade)}`}>
                                {student.grade}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
