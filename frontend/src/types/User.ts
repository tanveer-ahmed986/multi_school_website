/**
 * User type definitions for authentication and authorization
 */

export enum UserRole {
  SUPER_ADMIN = 'SUPER_ADMIN',
  SCHOOL_ADMIN = 'SCHOOL_ADMIN',
  STAFF = 'STAFF',
  PUBLIC = 'PUBLIC',
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  school_id?: string;
  created_at?: string;
  updated_at?: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}
