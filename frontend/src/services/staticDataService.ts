/**
 * Static Data Service - File-based data management
 *
 * This service reads school data from JSON files instead of a database.
 * Perfect for single-school deployments without backend infrastructure.
 *
 * Data files location: frontend/public/data/
 *
 * Usage:
 * import { staticDataService } from '@/services/staticDataService';
 * const principal = await staticDataService.getPrincipal();
 */

export interface SchoolConfig {
  school_name: string;
  tagline: string;
  logo_url: string;
  banner_url: string;
  primary_color: string;
  secondary_color: string;
  address: string;
  phone: string;
  email: string;
  established_year: number;
  total_students: number;
  total_teachers: number;
  facilities: string[];
  social_media: {
    facebook?: string;
    twitter?: string;
    instagram?: string;
    youtube?: string;
  };
}

export interface PrincipalProfile {
  principal_name: string;
  designation: string;
  qualification: string;
  experience_years: number;
  photo_url: string;
  email?: string;
  phone?: string;
  message: string;
}

export interface Faculty {
  id: string;
  name: string;
  designation: string;
  qualification: string;
  photo_url: string;
  email: string;
  subjects: string[];
  experience_years: number;
  is_visible: boolean;
}

export interface Notice {
  id: string;
  title: string;
  content: string;
  priority: 'high' | 'medium' | 'low';
  published_date: string;
  is_active: boolean;
}

export interface GalleryImage {
  id: string;
  title: string;
  description: string;
  image_url: string;
  category: string;
  upload_date: string;
}

export interface StudentResult {
  roll_no: string;
  name: string;
  marks: Record<string, number>;
  total: number;
  percentage: number;
  grade: string;
  rank: number;
}

export interface ExamResult {
  id: string;
  academic_year: string;
  class_level: string;
  exam_type: string;
  total_students: number;
  pass_percentage: number;
  average_marks: number;
  students: StudentResult[];
}

export class StaticDataService {
  private baseUrl = '/data';

  /**
   * Fetch and parse JSON data from a file
   */
  private async fetchJSON<T>(filename: string): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}/${filename}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch ${filename}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error loading ${filename}:`, error);
      throw error;
    }
  }

  /**
   * Get school configuration and branding
   */
  async getSchoolConfig(): Promise<SchoolConfig> {
    return this.fetchJSON<SchoolConfig>('school-config.json');
  }

  /**
   * Get principal profile and message
   */
  async getPrincipal(): Promise<PrincipalProfile> {
    return this.fetchJSON<PrincipalProfile>('principal.json');
  }

  /**
   * Get all visible faculty members
   */
  async getFaculty(): Promise<Faculty[]> {
    const data = await this.fetchJSON<Faculty[]>('faculty.json');
    return data.filter((faculty) => faculty.is_visible);
  }

  /**
   * Get active notices sorted by priority
   */
  async getNotices(): Promise<Notice[]> {
    const data = await this.fetchJSON<Notice[]>('notices.json');

    const priorityOrder = { high: 1, medium: 2, low: 3 };

    return data
      .filter((notice) => notice.is_active)
      .sort((a, b) => {
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      });
  }

  /**
   * Get gallery images with optional category filter
   */
  async getGallery(category?: string): Promise<GalleryImage[]> {
    const data = await this.fetchJSON<GalleryImage[]>('gallery.json');

    if (category) {
      return data.filter((image) => image.category === category);
    }

    return data;
  }

  /**
   * Get all exam results
   */
  async getResults(): Promise<ExamResult[]> {
    return this.fetchJSON<ExamResult[]>('results.json');
  }

  /**
   * Get specific result by ID
   */
  async getResultById(id: string): Promise<ExamResult | undefined> {
    const data = await this.fetchJSON<ExamResult[]>('results.json');
    return data.find((result) => result.id === id);
  }

  /**
   * Get result by academic year and class level
   */
  async getResultByYearAndClass(
    year: string,
    classLevel: string
  ): Promise<ExamResult | undefined> {
    const data = await this.fetchJSON<ExamResult[]>('results.json');
    return data.find(
      (result) =>
        result.academic_year === year && result.class_level === classLevel
    );
  }

  /**
   * Get unique academic years from results
   */
  async getAcademicYears(): Promise<string[]> {
    const data = await this.fetchJSON<ExamResult[]>('results.json');
    const years = data.map((result) => result.academic_year);
    return Array.from(new Set(years)).sort().reverse();
  }

  /**
   * Get unique class levels from results
   */
  async getClassLevels(): Promise<string[]> {
    const data = await this.fetchJSON<ExamResult[]>('results.json');
    const classes = data.map((result) => result.class_level);
    return Array.from(new Set(classes)).sort();
  }

  /**
   * Get gallery categories
   */
  async getGalleryCategories(): Promise<string[]> {
    const data = await this.fetchJSON<GalleryImage[]>('gallery.json');
    const categories = data.map((image) => image.category);
    return Array.from(new Set(categories)).sort();
  }
}

// Export singleton instance
export const staticDataService = new StaticDataService();
export default staticDataService;
