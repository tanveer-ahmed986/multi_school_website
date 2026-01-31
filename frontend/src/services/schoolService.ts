/**
 * School management service for super admin operations.
 * (T174 - Implementation)
 */
import axios, { AxiosInstance } from 'axios';
import { authService } from './authService';

interface School {
  school_id: string;
  school_name: string;
  subdomain: string;
  contact_email: string;
  contact_phone: string | null;
  address: string | null;
  logo_url: string | null;
  primary_color: string;
  secondary_color: string;
  is_active: boolean;
  storage_used_bytes: number;
  storage_limit_bytes: number;
}

interface CreateSchoolData {
  school_name: string;
  subdomain: string;
  contact_email: string;
  contact_phone?: string;
  address?: string;
  primary_color?: string;
  secondary_color?: string;
}

interface AssignAdminData {
  email: string;
  password: string;
  full_name: string;
}

class SchoolService {
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

  async createSchool(data: CreateSchoolData): Promise<School> {
    const response = await this.api.post('/schools', data);
    return response.data;
  }

  async listSchools(params?: {
    skip?: number;
    limit?: number;
    search?: string;
    is_active?: boolean;
  }): Promise<School[]> {
    const response = await this.api.get('/schools', { params });
    return response.data;
  }

  async getSchool(schoolId: string): Promise<School> {
    const response = await this.api.get(`/schools/${schoolId}`);
    return response.data;
  }

  async updateSchool(schoolId: string, data: Partial<School>): Promise<School> {
    const response = await this.api.put(`/schools/${schoolId}`, data);
    return response.data;
  }

  async assignAdmin(schoolId: string, data: AssignAdminData): Promise<any> {
    const response = await this.api.post(`/schools/${schoolId}/admins`, data);
    return response.data;
  }

  async deactivateSchool(schoolId: string): Promise<void> {
    await this.api.delete(`/schools/${schoolId}`);
  }
}

export const schoolService = new SchoolService();
export default schoolService;
