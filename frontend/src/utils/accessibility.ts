/**
 * Accessibility Utilities (T198)
 *
 * Utilities for ensuring WCAG 2.1 Level AA compliance:
 * - Contrast ratio calculation
 * - Color validation
 * - Accessibility helpers
 */

/**
 * Calculate relative luminance of a color
 * Based on WCAG 2.1 formula
 */
function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map((c) => {
    const sRGB = c / 255;
    return sRGB <= 0.03928 ? sRGB / 12.92 : Math.pow((sRGB + 0.055) / 1.055, 2.4);
  });

  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

/**
 * Parse hex color to RGB
 */
function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

/**
 * Calculate contrast ratio between two colors
 * Returns ratio (1-21)
 */
export function getContrastRatio(color1: string, color2: string): number {
  const rgb1 = hexToRgb(color1);
  const rgb2 = hexToRgb(color2);

  if (!rgb1 || !rgb2) {
    throw new Error('Invalid color format. Use hex colors (#RRGGBB)');
  }

  const lum1 = getLuminance(rgb1.r, rgb1.g, rgb1.b);
  const lum2 = getLuminance(rgb2.r, rgb2.g, rgb2.b);

  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);

  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check if contrast ratio meets WCAG AA standard (4.5:1 for normal text)
 */
export function meetsWCAG_AA(foreground: string, background: string): boolean {
  const ratio = getContrastRatio(foreground, background);
  return ratio >= 4.5;
}

/**
 * Check if contrast ratio meets WCAG AA standard for large text (3:1)
 */
export function meetsWCAG_AA_Large(foreground: string, background: string): boolean {
  const ratio = getContrastRatio(foreground, background);
  return ratio >= 3.0;
}

/**
 * Check if contrast ratio meets WCAG AAA standard (7:1)
 */
export function meetsWCAG_AAA(foreground: string, background: string): boolean {
  const ratio = getContrastRatio(foreground, background);
  return ratio >= 7.0;
}

/**
 * Validate school colors meet accessibility standards
 * Returns warnings if colors don't meet WCAG AA
 */
export function validateSchoolColors(
  primaryColor: string,
  secondaryColor: string
): { valid: boolean; warnings: string[] } {
  const warnings: string[] = [];

  // Check primary color against white (for text)
  if (!meetsWCAG_AA(primaryColor, '#FFFFFF')) {
    warnings.push(
      `Primary color (${primaryColor}) does not have sufficient contrast with white text (ratio: ${getContrastRatio(primaryColor, '#FFFFFF').toFixed(2)}:1, required: 4.5:1)`
    );
  }

  // Check secondary color against white (for text)
  if (!meetsWCAG_AA(secondaryColor, '#FFFFFF')) {
    warnings.push(
      `Secondary color (${secondaryColor}) does not have sufficient contrast with white text (ratio: ${getContrastRatio(secondaryColor, '#FFFFFF').toFixed(2)}:1, required: 4.5:1)`
    );
  }

  // Check primary and secondary color contrast
  if (!meetsWCAG_AA(primaryColor, secondaryColor)) {
    warnings.push(
      `Primary and secondary colors do not have sufficient contrast (ratio: ${getContrastRatio(primaryColor, secondaryColor).toFixed(2)}:1, required: 4.5:1)`
    );
  }

  return {
    valid: warnings.length === 0,
    warnings,
  };
}

/**
 * Get accessible text color (black or white) for a background color
 */
export function getAccessibleTextColor(backgroundColor: string): string {
  const whiteContrast = getContrastRatio('#FFFFFF', backgroundColor);
  const blackContrast = getContrastRatio('#000000', backgroundColor);

  return whiteContrast > blackContrast ? '#FFFFFF' : '#000000';
}
