/**
 * Gallery grid component with lazy loading and lightbox.
 * (T087 - Implementation)
 */
'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import type { GalleryImage } from '../../types/Gallery';

interface GalleryGridProps {
  images: GalleryImage[];
}

export function GalleryGrid({ images }: GalleryGridProps) {
  const [selectedImage, setSelectedImage] = useState<GalleryImage | null>(null);

  if (images.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No images available in this category.
      </div>
    );
  }

  return (
    <>
      <div data-testid="gallery-grid" className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {images.map((image) => (
          <div
            key={image.image_id}
            data-testid="gallery-image"
            className="group relative bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
            onClick={() => setSelectedImage(image)}
          >
            <div className="relative h-64">
              <Image
                src={image.thumbnail_url || image.image_url}
                alt={image.caption || 'Gallery image'}
                fill
                loading="lazy"
                className="object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>

            {image.caption && (
              <div data-testid="image-caption" className="p-3 bg-white">
                <p className="text-sm text-gray-700 line-clamp-2">{image.caption}</p>
                {image.event_date && (
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(image.event_date).toLocaleDateString()}
                  </p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Lightbox Modal */}
      {selectedImage && (
        <div
          data-testid="image-lightbox"
          className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <button
            className="absolute top-4 right-4 text-white text-4xl font-bold hover:text-gray-300"
            onClick={() => setSelectedImage(null)}
            aria-label="Close lightbox"
          >
            ×
          </button>

          <div className="max-w-5xl max-h-full flex flex-col items-center">
            <div className="relative w-full" style={{ maxHeight: '80vh' }}>
              <Image
                src={selectedImage.image_url}
                alt={selectedImage.caption || 'Gallery image'}
                width={1200}
                height={800}
                className="object-contain max-h-screen"
                onClick={(e) => e.stopPropagation()}
              />
            </div>

            {selectedImage.caption && (
              <div className="mt-4 text-white text-center">
                <p className="text-lg">{selectedImage.caption}</p>
                {selectedImage.event_date && (
                  <p className="text-sm text-gray-300 mt-1">
                    {new Date(selectedImage.event_date).toLocaleDateString()}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
