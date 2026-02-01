/**
 * Gallery page - Display school photos with category filtering.
 * (T077 - Implementation)
 */
'use client';

import React, { useEffect, useState } from 'react';
import { publicService } from '../../services/publicService';
import { GalleryGrid } from '../../components/public/GalleryGrid';
import type { GalleryImage, GalleryCategory } from '../../types/Gallery';
import { GALLERY_CATEGORIES } from '../../types/Gallery';

export default function GalleryPage() {
  const [images, setImages] = useState<GalleryImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  useEffect(() => {
    fetchGallery();
  }, [selectedCategory]);

  const fetchGallery = async () => {
    try {
      setLoading(true);
      const response = await fetch('/data/gallery.json');
      const rawData = await response.json();

      // Map static data to GalleryImage type
      let mappedData = rawData.map((item: any) => ({
        image_id: item.id,
        category: item.category.toLowerCase(),
        image_url: item.image_url,
        thumbnail_url: null,
        caption: item.title,
        event_date: item.upload_date
      }));

      // Filter by category if selected
      if (selectedCategory) {
        mappedData = mappedData.filter((img: GalleryImage) => img.category === selectedCategory);
      }

      setImages(mappedData);
    } catch (error) {
      console.error('Failed to fetch gallery:', error);
      setImages([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Photo Gallery</h1>

      {/* Category Filters */}
      <div className="flex flex-wrap gap-3 mb-8">
        <button
          data-testid="category-filter"
          data-category="all"
          onClick={() => setSelectedCategory('')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            selectedCategory === ''
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All
        </button>
        {GALLERY_CATEGORIES.map((category) => (
          <button
            key={category}
            data-testid="category-filter"
            data-category={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-lg font-medium capitalize transition-colors ${
              selectedCategory === category
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Gallery Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="h-64 bg-gray-200 animate-pulse"></div>
              <div className="p-3 space-y-2">
                <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3 animate-pulse"></div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <GalleryGrid images={images} />
      )}
    </div>
  );
}
