/**
 * ColorPreview component for live theme preview.
 * (T183 - Implementation)
 *
 * Displays a live preview of how primary and secondary colors
 * will appear on various UI elements (headers, buttons, backgrounds).
 */
'use client';

import React from 'react';

interface ColorPreviewProps {
  primaryColor: string;
  secondaryColor: string;
  logoUrl?: string;
}

export function ColorPreview({ primaryColor, secondaryColor, logoUrl }: ColorPreviewProps) {
  return (
    <div className="space-y-4" data-testid="color-preview">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Live Preview</h3>

      {/* Header Preview */}
      <div
        data-testid="preview-header"
        style={{ backgroundColor: primaryColor }}
        className="p-4 rounded-lg text-white shadow-sm"
      >
        <div className="flex items-center space-x-2">
          {logoUrl && (
            <img
              src={logoUrl}
              alt="Logo preview"
              className="h-8 w-8 object-contain bg-white/10 rounded"
              onError={(e) => {
                (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          )}
          <div>
            <p className="font-bold text-base">Header</p>
            <p className="text-xs opacity-90">Navigation bar with primary color</p>
          </div>
        </div>
      </div>

      {/* Button Preview */}
      <div className="space-y-2">
        <button
          data-testid="preview-button"
          style={{ backgroundColor: primaryColor }}
          className="w-full py-2.5 px-4 rounded-lg text-white font-medium shadow-sm hover:opacity-90 transition-opacity"
        >
          Primary Button
        </button>
        <p className="text-xs text-gray-500 text-center">
          Call-to-action and primary actions
        </p>
      </div>

      {/* Secondary Background Preview */}
      <div
        data-testid="preview-secondary-bg"
        style={{ backgroundColor: secondaryColor }}
        className="p-4 rounded-lg shadow-sm"
      >
        <p className="text-gray-800 font-medium text-sm">Secondary Background</p>
        <p className="text-xs text-gray-600 mt-1">
          Used for sections, cards, and highlighted areas
        </p>
      </div>

      {/* Card with Border Preview */}
      <div className="border-2 rounded-lg p-4" style={{ borderColor: primaryColor }}>
        <p className="text-sm font-medium text-gray-700">Card with Primary Border</p>
        <p className="text-xs text-gray-500 mt-1">Accent and focus indicators</p>
      </div>

      {/* Link Text Preview */}
      <div className="p-3 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-700">
          Sample text with{' '}
          <span style={{ color: primaryColor }} className="font-semibold underline cursor-pointer">
            primary color link
          </span>
        </p>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
        <p className="text-xs text-blue-800">
          <strong>Tip:</strong> Preview updates in real-time as you adjust colors. Make sure there's
          sufficient contrast between text and background for accessibility.
        </p>
      </div>
    </div>
  );
}
