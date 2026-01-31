/**
 * Authentication service for admin login/logout.
 * (T138 - Implementation)
 */
import axios, { AxiosInstance } from 'axios';

interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    user_id: string;
    email: string;
    full_name: string;
    role: string;
    school_id: string | null;
  };
}

class AuthService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, // Important for HTTP-only cookies
    });
  }

  /**
   * Login with email and password.
   * Stores access token in localStorage and refresh token in HTTP-only cookie.
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await this.api.post<LoginResponse>('/auth/login', credentials);

    // Store access token in localStorage
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    return response.data;
  }

  /**
   * Refresh access token using refresh token cookie.
   */
  async refresh(): Promise<LoginResponse> {
    const response = await this.api.post<LoginResponse>('/auth/refresh');

    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    return response.data;
  }

  /**
   * Logout user and clear tokens.
   */
  async logout(): Promise<void> {
    try {
      await this.api.post('/auth/logout');
    } finally {
      // Clear local storage even if API call fails
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
  }

  /**
   * Get current access token from localStorage.
   */
  getAccessToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  /**
   * Get current user from localStorage.
   */
  getCurrentUser(): LoginResponse['user'] | null {
    if (typeof window === 'undefined') return null;
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * Check if user is authenticated.
   */
  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }
}

export const authService = new AuthService();
export default authService;
