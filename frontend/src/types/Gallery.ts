/**
 * Gallery image type definition
 */
export interface GalleryImage {
  image_id: string;
  category: string;
  image_url: string;
  thumbnail_url: string | null;
  caption: string | null;
  event_date: string | null;
}

export type GalleryCategory = 'sports' | 'cultural' | 'academics' | 'events' | 'infrastructure';

export const GALLERY_CATEGORIES: GalleryCategory[] = [
  'sports',
  'cultural',
  'academics',
  'events',
  'infrastructure'
];
