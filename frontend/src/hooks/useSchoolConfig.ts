/**
 * Custom hook to fetch and cache school configuration.
 * (T094 - Implementation)
 */
'use client';

import { useState, useEffect } from 'react';
import { publicService } from '../services/publicService';
import type { School } from '../types/School';

interface UseSchoolConfigReturn {
  config: School | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

/**
 * Fetch school configuration from API and cache in state.
 * Automatically refetches when component mounts.
 *
 * @returns School configuration with loading and error states
 */
export function useSchoolConfig(): UseSchoolConfigReturn {
  const [config, setConfig] = useState<School | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchConfig = async () => {
    try {
      setLoading(true);
      setError(null);
      const schoolConfig = await publicService.getSchoolInfo();
      setConfig(schoolConfig);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch school config'));
      setConfig(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConfig();
  }, []);

  return {
    config,
    loading,
    error,
    refetch: fetchConfig,
  };
}
