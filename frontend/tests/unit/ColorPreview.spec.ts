/**
 * Unit tests for ColorPreview component.
 * (T182 - Implementation)
 *
 * Tests cover:
 * - Rendering with provided colors
 * - Live preview of theme changes
 * - Color application to various UI elements
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ColorPreview } from '../../src/components/admin/ColorPreview';

describe('ColorPreview', () => {
  it('should render with default colors', () => {
    const { container } = render(
      <ColorPreview primaryColor="#0A3D62" secondaryColor="#EAF2F8" />
    );

    expect(container).toBeTruthy();
  });

  it('should apply primary color to header preview', () => {
    render(<ColorPreview primaryColor="#FF5733" secondaryColor="#EAF2F8" />);

    const headerPreview = screen.getByTestId('preview-header');
    expect(headerPreview).toHaveStyle({ backgroundColor: '#FF5733' });
  });

  it('should apply primary color to button preview', () => {
    render(<ColorPreview primaryColor="#1E88E5" secondaryColor="#EAF2F8" />);

    const buttonPreview = screen.getByTestId('preview-button');
    expect(buttonPreview).toHaveStyle({ backgroundColor: '#1E88E5' });
  });

  it('should apply secondary color to background preview', () => {
    render(<ColorPreview primaryColor="#0A3D62" secondaryColor="#C70039" />);

    const backgroundPreview = screen.getByTestId('preview-secondary-bg');
    expect(backgroundPreview).toHaveStyle({ backgroundColor: '#C70039' });
  });

  it('should update colors when props change', () => {
    const { rerender } = render(
      <ColorPreview primaryColor="#000000" secondaryColor="#FFFFFF" />
    );

    let headerPreview = screen.getByTestId('preview-header');
    expect(headerPreview).toHaveStyle({ backgroundColor: '#000000' });

    // Update colors
    rerender(<ColorPreview primaryColor="#FF0000" secondaryColor="#00FF00" />);

    headerPreview = screen.getByTestId('preview-header');
    expect(headerPreview).toHaveStyle({ backgroundColor: '#FF0000' });
  });

  it('should display preview labels', () => {
    render(<ColorPreview primaryColor="#0A3D62" secondaryColor="#EAF2F8" />);

    expect(screen.getByText(/header/i)).toBeInTheDocument();
    expect(screen.getByText(/primary button/i)).toBeInTheDocument();
    expect(screen.getByText(/secondary background/i)).toBeInTheDocument();
  });

  it('should handle hex color codes with uppercase letters', () => {
    render(<ColorPreview primaryColor="#ABCDEF" secondaryColor="#123456" />);

    const headerPreview = screen.getByTestId('preview-header');
    expect(headerPreview).toHaveStyle({ backgroundColor: '#ABCDEF' });
  });

  it('should render multiple preview elements', () => {
    render(<ColorPreview primaryColor="#0A3D62" secondaryColor="#EAF2F8" />);

    expect(screen.getByTestId('preview-header')).toBeInTheDocument();
    expect(screen.getByTestId('preview-button')).toBeInTheDocument();
    expect(screen.getByTestId('preview-secondary-bg')).toBeInTheDocument();
  });
});
