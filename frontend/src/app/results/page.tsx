/**
 * Results page - Display published results with filtering.
 * (T076 - Implementation)
 */
'use client';

import React, { useEffect, useState } from 'react';
import { publicService } from '../../services/publicService';
import { ResultsTable } from '../../components/public/ResultsTable';
import type { Result, ResultSummary } from '../../types/Result';

export default function ResultsPage() {
  const [results, setResults] = useState<ResultSummary[]>([]);
  const [selectedResult, setSelectedResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(true);
  const [yearFilter, setYearFilter] = useState<string>('');
  const [classFilter, setClassFilter] = useState<string>('');

  useEffect(() => {
    fetchResults();
  }, [yearFilter, classFilter]);

  const fetchResults = async () => {
    try {
      setLoading(true);
      const filters: any = {};
      if (yearFilter) filters.year = yearFilter;
      if (classFilter) filters.class_level = classFilter;

      const data = await publicService.getResults(filters);
      setResults(data);
    } catch (error) {
      console.error('Failed to fetch results:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleResultClick = async (result: ResultSummary) => {
    try {
      const fullResult = await publicService.getSpecificResult(
        result.academic_year,
        result.class_level
      );
      setSelectedResult(fullResult);
    } catch (error) {
      console.error('Failed to fetch result details:', error);
    }
  };

  // Extract unique years and classes for filters
  const uniqueYears = Array.from(new Set(results.map((r) => r.academic_year)));
  const uniqueClasses = Array.from(new Set(results.map((r) => r.class_level)));

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Examination Results</h1>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="year-filter" className="block text-sm font-medium text-gray-700 mb-2">
              Academic Year
            </label>
            <select
              id="year-filter"
              data-testid="year-filter"
              value={yearFilter}
              onChange={(e) => setYearFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Years</option>
              {uniqueYears.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="class-filter" className="block text-sm font-medium text-gray-700 mb-2">
              Class
            </label>
            <select
              id="class-filter"
              data-testid="class-filter"
              value={classFilter}
              onChange={(e) => setClassFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Classes</option>
              {uniqueClasses.map((cls) => (
                <option key={cls} value={cls}>
                  {cls}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Results List */}
      {loading ? (
        <div data-testid="results-list" className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-white p-6 rounded-lg shadow animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/3 mb-3"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      ) : results.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No results available for the selected filters.
        </div>
      ) : (
        <div data-testid="results-list" className="space-y-4">
          {results.map((result) => (
            <div
              key={result.result_id}
              data-testid="result-card"
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => handleResultClick(result)}
            >
              <h3 className="text-xl font-bold text-gray-800 mb-2">
                {result.class_level} - {result.exam_type}
              </h3>
              <p className="text-gray-600 mb-1">
                <span className="font-semibold">Academic Year:</span> {result.academic_year}
              </p>
              <p className="text-gray-500 text-sm">
                Published: {new Date(result.published_date).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Result Details Modal */}
      {selectedResult && (
        <div
          data-testid="result-details"
          className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => setSelectedResult(null)}
        >
          <div
            className="bg-white rounded-lg shadow-xl max-w-6xl w-full my-8 p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-800">
                  {selectedResult.class_level} - {selectedResult.exam_type}
                </h2>
                <p className="text-gray-600">Academic Year: {selectedResult.academic_year}</p>
              </div>
              <button
                onClick={() => setSelectedResult(null)}
                className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
                aria-label="Close"
              >
                ×
              </button>
            </div>

            <ResultsTable result={selectedResult} />
          </div>
        </div>
      )}
    </div>
  );
}
