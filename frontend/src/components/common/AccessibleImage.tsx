/**
 * Accessible Image Component (T200)
 *
 * Wrapper around Next.js Image component with:
 * - Required alt text
 * - Decorative image support (alt="")
 * - Loading states with screen reader announcements
 */

'use client';

import Image, { ImageProps } from 'next/image';
import { useState } from 'react';

interface AccessibleImageProps extends Omit<ImageProps, 'alt'> {
  alt: string;
  isDecorative?: boolean;
  caption?: string;
}

export function AccessibleImage({
  alt,
  isDecorative = false,
  caption,
  className = '',
  ...props
}: AccessibleImageProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const effectiveAlt = isDecorative ? '' : alt;

  if (hasError) {
    return (
      <div
        className={`bg-gray-200 flex items-center justify-center ${className}`}
        role="img"
        aria-label={`Failed to load image${alt ? `: ${alt}` : ''}`}
      >
        <span className="text-gray-500 text-sm">Image unavailable</span>
      </div>
    );
  }

  return (
    <figure className={caption ? 'relative' : undefined}>
      <div className="relative">
        {isLoading && (
          <div
            className="absolute inset-0 bg-gray-200 animate-pulse"
            aria-label="Image loading"
          />
        )}
        <Image
          alt={effectiveAlt}
          onLoad={() => setIsLoading(false)}
          onError={() => {
            setIsLoading(false);
            setHasError(true);
          }}
          className={className}
          {...props}
        />
      </div>
      {caption && (
        <figcaption className="text-sm text-gray-600 mt-2">{caption}</figcaption>
      )}
    </figure>
  );
}
