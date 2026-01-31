/**
 * Public API service for school website visitors.
 * Handles all read-only API calls to backend public endpoints.
 * (T091 - Implementation)
 */
import axios, { AxiosInstance } from 'axios';
import type { School } from '../types/School';
import type { Faculty } from '../types/Faculty';
import type { Result, ResultSummary } from '../types/Result';
import type { Notice } from '../types/Notice';
import type { GalleryImage } from '../types/Gallery';
import type { PrincipalProfile } from '../types/Principal';

class PublicService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include Host header with subdomain
    this.api.interceptors.request.use((config) => {
      // Extract subdomain from window.location.hostname
      if (typeof window !== 'undefined') {
        config.headers['Host'] = window.location.hostname;
      }
      return config;
    });
  }

  /**
   * Get school information and branding configuration.
   */
  async getSchoolInfo(): Promise<School> {
    const response = await this.api.get<School>('/public/school');
    return response.data;
  }

  /**
   * Get visible faculty members for the school.
   */
  async getFaculty(): Promise<Faculty[]> {
    const response = await this.api.get<Faculty[]>('/public/faculty');
    return response.data;
  }

  /**
   * Get published results with optional filters.
   */
  async getResults(filters?: {
    year?: string;
    class_level?: string;
  }): Promise<ResultSummary[]> {
    const params = new URLSearchParams();
    if (filters?.year) params.append('year', filters.year);
    if (filters?.class_level) params.append('class_level', filters.class_level);

    const response = await this.api.get<ResultSummary[]>(
      `/public/results?${params.toString()}`
    );
    return response.data;
  }

  /**
   * Get specific result details by year and class.
   */
  async getSpecificResult(year: string, classLevel: string): Promise<Result> {
    const response = await this.api.get<Result>(
      `/public/results/${encodeURIComponent(year)}/${encodeURIComponent(classLevel)}`
    );
    return response.data;
  }

  /**
   * Get active notices sorted by priority.
   */
  async getNotices(): Promise<Notice[]> {
    const response = await this.api.get<Notice[]>('/public/notices');
    return response.data;
  }

  /**
   * Get gallery images with optional category filter.
   */
  async getGallery(category?: string): Promise<GalleryImage[]> {
    const params = category ? `?category=${encodeURIComponent(category)}` : '';
    const response = await this.api.get<GalleryImage[]>(`/public/gallery${params}`);
    return response.data;
  }

  /**
   * Get principal profile.
   */
  async getPrincipal(): Promise<PrincipalProfile> {
    const response = await this.api.get<PrincipalProfile>('/public/principal');
    return response.data;
  }
}

// Export singleton instance
export const publicService = new PublicService();
export default publicService;
