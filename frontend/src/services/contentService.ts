/**
 * Content management service for admin operations.
 * (T157 - Implementation)
 */
import axios, { AxiosInstance } from 'axios';
import { authService } from './authService';
import type { Faculty } from '../types/Faculty';
import type { Result, ResultSummary } from '../types/Result';
import type { Notice } from '../types/Notice';
import type { GalleryImage } from '../types/Gallery';
import type { PrincipalProfile } from '../types/Principal';

class ContentService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      withCredentials: true,
    });

    // Add auth token to requests
    this.api.interceptors.request.use((config) => {
      const token = authService.getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // ========== Faculty Management ==========

  async createFaculty(data: Partial<Faculty>): Promise<Faculty> {
    const response = await this.api.post('/content/faculty', data);
    return response.data;
  }

  async updateFaculty(id: string, data: Partial<Faculty>): Promise<Faculty> {
    const response = await this.api.put(`/content/faculty/${id}`, data);
    return response.data;
  }

  async deleteFaculty(id: string): Promise<void> {
    await this.api.delete(`/content/faculty/${id}`);
  }

  async listFaculty(includeHidden: boolean = true): Promise<Faculty[]> {
    const response = await this.api.get(`/content/faculty?include_hidden=${includeHidden}`);
    return response.data;
  }

  // ========== Results Management ==========

  async createResult(data: {
    academic_year: string;
    class_level: string;
    exam_type: string;
    result_data: any;
    is_published: boolean;
  }): Promise<{ result_id: string; message: string }> {
    const response = await this.api.post('/content/results', data);
    return response.data;
  }

  async updateResult(id: string, data: {
    result_data?: any;
    is_published?: boolean;
  }): Promise<{ message: string }> {
    const response = await this.api.put(`/content/results/${id}`, data);
    return response.data;
  }

  // ========== Notices Management ==========

  async createNotice(data: Partial<Notice>): Promise<{ notice_id: string; message: string }> {
    const response = await this.api.post('/content/notices', data);
    return response.data;
  }

  async updateNotice(id: string, data: Partial<Notice>): Promise<{ message: string }> {
    const response = await this.api.put(`/content/notices/${id}`, data);
    return response.data;
  }

  // ========== Gallery Management ==========

  async uploadGalleryImage(data: {
    category: string;
    image_url: string;
    thumbnail_url?: string;
    caption?: string;
    file_size_bytes: number;
  }): Promise<{ image_id: string; message: string }> {
    const response = await this.api.post('/content/gallery', data);
    return response.data;
  }

  async deleteGalleryImage(id: string): Promise<void> {
    await this.api.delete(`/content/gallery/${id}`);
  }

  // ========== Principal Profile ==========

  async updatePrincipalProfile(data: Partial<PrincipalProfile>): Promise<{ message: string }> {
    const response = await this.api.put('/content/principal', data);
    return response.data;
  }

  async getPrincipalProfile(): Promise<PrincipalProfile> {
    const response = await this.api.get('/content/principal');
    return response.data;
  }

  // ========== School Branding ==========

  async updateBranding(data: {
    logo_url?: string;
    primary_color?: string;
    secondary_color?: string;
    contact_email?: string;
    contact_phone?: string;
    address?: string;
  }): Promise<{
    school_id: string;
    school_name: string;
    subdomain: string;
    logo_url: string | null;
    primary_color: string;
    secondary_color: string;
    contact_email: string;
    contact_phone: string | null;
    address: string | null;
  }> {
    const response = await this.api.put('/content/branding', data);
    return response.data;
  }
}

export const contentService = new ContentService();
export default contentService;
