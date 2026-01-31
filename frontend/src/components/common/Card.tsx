/**
 * Accessible Card Component (T196)
 *
 * Features:
 * - Semantic HTML structure
 * - Optional ARIA labels
 * - Keyboard navigation for interactive cards
 */

'use client';

import { HTMLAttributes, ReactNode } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  isInteractive?: boolean;
  ariaLabel?: string;
}

export function Card({
  children,
  isInteractive = false,
  ariaLabel,
  className = '',
  ...props
}: CardProps) {
  const baseStyles = 'bg-white rounded-lg shadow-md p-6';
  const interactiveStyles = isInteractive
    ? 'hover:shadow-lg transition-shadow cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500'
    : '';

  return (
    <div
      className={`${baseStyles} ${interactiveStyles} ${className}`}
      role={isInteractive ? 'button' : undefined}
      tabIndex={isInteractive ? 0 : undefined}
      aria-label={ariaLabel}
      {...props}
    >
      {children}
    </div>
  );
}
