/**
 * Principal profile type definition
 */
export interface PrincipalProfile {
  principal_name: string;
  photo_url: string | null;
  message_text: string;
  qualification: string | null;
  email: string | null;
  phone: string | null;
}
