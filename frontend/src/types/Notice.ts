/**
 * Notice entity type definition
 */
export interface Notice {
  notice_id: string;
  title: string;
  description: string;
  priority_level: number;
  category: string;
  published_date: string;
  expiry_date: string | null;
  attachment_url: string | null;
}

export type NoticePriority = 0 | 1 | 2 | 3 | 4 | 5;

export const PRIORITY_LABELS: Record<NoticePriority, string> = {
  0: 'Low',
  1: 'Normal',
  2: 'Important',
  3: 'High',
  4: 'Very High',
  5: 'Urgent'
};

export const PRIORITY_COLORS: Record<NoticePriority, string> = {
  0: 'bg-gray-100 text-gray-800',
  1: 'bg-blue-100 text-blue-800',
  2: 'bg-yellow-100 text-yellow-800',
  3: 'bg-orange-100 text-orange-800',
  4: 'bg-red-100 text-red-800',
  5: 'bg-red-600 text-white'
};
