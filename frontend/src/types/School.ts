/**
 * School entity type definition
 */
export interface School {
  school_id: string;
  school_name: string;
  subdomain: string;
  logo_url: string | null;
  primary_color: string;
  secondary_color: string;
  contact_email: string;
  contact_phone: string | null;
  address: string | null;
}

export interface SchoolConfig extends School {
  // Additional configuration fields can be added here
}
