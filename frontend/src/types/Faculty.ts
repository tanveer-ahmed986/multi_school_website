/**
 * Faculty member type definition
 */
export interface Faculty {
  faculty_id: string;
  full_name: string;
  designation: string;
  qualification: string;
  experience_years: number;
  subject: string | null;
  photo_url: string | null;
  email: string | null;
  phone: string | null;
  bio: string | null;
}
