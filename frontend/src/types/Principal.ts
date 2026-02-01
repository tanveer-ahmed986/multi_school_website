/**
 * Principal profile type definition
 */
export interface PrincipalProfile {
  principal_name: string;
  designation?: string;
  qualification: string | null;
  experience_years?: number;
  photo_url: string | null;
  message: string;
  email?: string | null;
  phone?: string | null;
}
