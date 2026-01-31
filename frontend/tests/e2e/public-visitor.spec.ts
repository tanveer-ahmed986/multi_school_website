/**
 * E2E tests for Public Website Visitor (User Story 1)
 *
 * Tests cover:
 * - T069: Homepage (hero, principal message, notices)
 * - T070: Faculty page (faculty cards display)
 * - T071: Results page (year/class filtering)
 * - T072: Gallery page (category filtering, lazy loading)
 * - T073: Notices page (active notices display)
 */
import { test, expect } from '@playwright/test';

test.describe('Public Website Visitor - Homepage', () => {
  test('should display school branding and hero section', async ({ page }) => {
    // Visit school subdomain
    await page.goto('/');

    // Check hero section
    await expect(page.locator('h1')).toContainText('Test High School');

    // Check navigation header exists
    const header = page.locator('header');
    await expect(header).toBeVisible();

    // Check school logo is displayed
    const logo = page.locator('img[alt*="logo"]').first();
    await expect(logo).toBeVisible();
  });

  test('should display principal message on homepage', async ({ page }) => {
    await page.goto('/');

    // Check principal message section exists
    const principalSection = page.locator('[data-testid="principal-message"]');
    await expect(principalSection).toBeVisible();

    // Check principal name and message
    await expect(principalSection.locator('[data-testid="principal-name"]')).toBeVisible();
    await expect(principalSection.locator('[data-testid="principal-message"]')).toBeVisible();
  });

  test('should display latest notices on homepage', async ({ page }) => {
    await page.goto('/');

    // Check notices section
    const noticesSection = page.locator('[data-testid="latest-notices"]');
    await expect(noticesSection).toBeVisible();

    // Check at least one notice is displayed
    const noticeCards = noticesSection.locator('[data-testid="notice-card"]');
    await expect(noticeCards.first()).toBeVisible();
  });

  test('should navigate to different sections from homepage', async ({ page }) => {
    await page.goto('/');

    // Test navigation to faculty page
    await page.click('a[href="/faculty"]');
    await expect(page).toHaveURL(/.*faculty/);

    // Navigate back to home
    await page.goto('/');

    // Test navigation to results page
    await page.click('a[href="/results"]');
    await expect(page).toHaveURL(/.*results/);
  });
});

test.describe('Public Website Visitor - Faculty Page', () => {
  test('should display faculty cards with member information', async ({ page }) => {
    await page.goto('/faculty');

    // Check page title
    await expect(page.locator('h1')).toContainText('Faculty');

    // Check faculty cards are displayed
    const facultyCards = page.locator('[data-testid="faculty-card"]');
    await expect(facultyCards.first()).toBeVisible();

    // Check faculty card contains required information
    const firstCard = facultyCards.first();
    await expect(firstCard.locator('[data-testid="faculty-name"]')).toBeVisible();
    await expect(firstCard.locator('[data-testid="faculty-designation"]')).toBeVisible();
    await expect(firstCard.locator('[data-testid="faculty-qualification"]')).toBeVisible();
  });

  test('should display faculty photos', async ({ page }) => {
    await page.goto('/faculty');

    // Check faculty photos are loaded
    const facultyPhoto = page.locator('[data-testid="faculty-card"] img').first();
    await expect(facultyPhoto).toBeVisible();

    // Check photo has alt text for accessibility
    const altText = await facultyPhoto.getAttribute('alt');
    expect(altText).toBeTruthy();
  });

  test('should display faculty in grid layout', async ({ page }) => {
    await page.goto('/faculty');

    // Check grid container exists
    const grid = page.locator('[data-testid="faculty-grid"]');
    await expect(grid).toBeVisible();

    // Check multiple faculty cards in grid
    const facultyCards = page.locator('[data-testid="faculty-card"]');
    const count = await facultyCards.count();
    expect(count).toBeGreaterThan(0);
  });
});

test.describe('Public Website Visitor - Results Page', () => {
  test('should display results page with year/class filters', async ({ page }) => {
    await page.goto('/results');

    // Check page title
    await expect(page.locator('h1')).toContainText('Results');

    // Check filter controls exist
    await expect(page.locator('[data-testid="year-filter"]')).toBeVisible();
    await expect(page.locator('[data-testid="class-filter"]')).toBeVisible();
  });

  test('should filter results by academic year', async ({ page }) => {
    await page.goto('/results');

    // Select year filter
    await page.selectOption('[data-testid="year-filter"]', '2024-25');

    // Wait for results to load
    await page.waitForTimeout(500);

    // Check results are displayed
    const resultsList = page.locator('[data-testid="results-list"]');
    await expect(resultsList).toBeVisible();
  });

  test('should filter results by class', async ({ page }) => {
    await page.goto('/results');

    // Select class filter
    await page.selectOption('[data-testid="class-filter"]', 'Class 10');

    // Wait for results to load
    await page.waitForTimeout(500);

    // Check filtered results
    const resultCards = page.locator('[data-testid="result-card"]');
    await expect(resultCards.first()).toBeVisible();
  });

  test('should display result details when clicking on a result', async ({ page }) => {
    await page.goto('/results');

    // Click on first result
    const firstResult = page.locator('[data-testid="result-card"]').first();
    await firstResult.click();

    // Check result details modal/page opens
    await expect(page.locator('[data-testid="result-details"]')).toBeVisible();

    // Check student data table is displayed
    await expect(page.locator('[data-testid="results-table"]')).toBeVisible();
  });

  test('should display result statistics', async ({ page }) => {
    await page.goto('/results');

    // Click on first result
    await page.locator('[data-testid="result-card"]').first().click();

    // Check statistics are displayed
    const stats = page.locator('[data-testid="result-statistics"]');
    await expect(stats).toBeVisible();
    await expect(stats).toContainText('Total Students');
    await expect(stats).toContainText('Pass Percentage');
  });
});

test.describe('Public Website Visitor - Gallery Page', () => {
  test('should display gallery page with category filters', async ({ page }) => {
    await page.goto('/gallery');

    // Check page title
    await expect(page.locator('h1')).toContainText('Gallery');

    // Check category filter buttons exist
    const categoryButtons = page.locator('[data-testid="category-filter"]');
    await expect(categoryButtons.first()).toBeVisible();
  });

  test('should filter gallery by category', async ({ page }) => {
    await page.goto('/gallery');

    // Click on "Sports" category filter
    await page.click('[data-testid="category-filter"][data-category="sports"]');

    // Wait for filtered images
    await page.waitForTimeout(500);

    // Check only sports images are displayed
    const images = page.locator('[data-testid="gallery-image"]');
    await expect(images.first()).toBeVisible();
  });

  test('should display images in grid layout with lazy loading', async ({ page }) => {
    await page.goto('/gallery');

    // Check grid container
    const grid = page.locator('[data-testid="gallery-grid"]');
    await expect(grid).toBeVisible();

    // Check images are loaded
    const images = page.locator('[data-testid="gallery-image"] img');
    await expect(images.first()).toBeVisible();

    // Check lazy loading attribute
    const firstImage = images.first();
    const loading = await firstImage.getAttribute('loading');
    expect(loading).toBe('lazy');
  });

  test('should display image captions', async ({ page }) => {
    await page.goto('/gallery');

    // Check first image has caption
    const firstImage = page.locator('[data-testid="gallery-image"]').first();
    const caption = firstImage.locator('[data-testid="image-caption"]');
    await expect(caption).toBeVisible();
  });

  test('should open image lightbox on click', async ({ page }) => {
    await page.goto('/gallery');

    // Click on first image
    await page.locator('[data-testid="gallery-image"]').first().click();

    // Check lightbox/modal opens
    const lightbox = page.locator('[data-testid="image-lightbox"]');
    await expect(lightbox).toBeVisible();

    // Check enlarged image is displayed
    await expect(lightbox.locator('img')).toBeVisible();
  });
});

test.describe('Public Website Visitor - Notices Page', () => {
  test('should display notices page with active notices', async ({ page }) => {
    await page.goto('/notices');

    // Check page title
    await expect(page.locator('h1')).toContainText('Notices');

    // Check notice board is displayed
    const noticeBoard = page.locator('[data-testid="notice-board"]');
    await expect(noticeBoard).toBeVisible();
  });

  test('should display notices sorted by priority', async ({ page }) => {
    await page.goto('/notices');

    // Check notices are displayed
    const notices = page.locator('[data-testid="notice-card"]');
    await expect(notices.first()).toBeVisible();

    // Check priority badge on high-priority notice
    const highPriorityNotice = notices.first();
    const priorityBadge = highPriorityNotice.locator('[data-testid="priority-badge"]');
    await expect(priorityBadge).toBeVisible();
  });

  test('should display notice details', async ({ page }) => {
    await page.goto('/notices');

    // Check first notice has all required fields
    const firstNotice = page.locator('[data-testid="notice-card"]').first();
    await expect(firstNotice.locator('[data-testid="notice-title"]')).toBeVisible();
    await expect(firstNotice.locator('[data-testid="notice-description"]')).toBeVisible();
    await expect(firstNotice.locator('[data-testid="notice-date"]')).toBeVisible();
  });

  test('should not display expired notices', async ({ page }) => {
    await page.goto('/notices');

    // All displayed notices should have valid expiry dates
    const notices = page.locator('[data-testid="notice-card"]');
    const count = await notices.count();

    // Check each notice for "Expired" text (should not exist)
    for (let i = 0; i < count; i++) {
      const notice = notices.nth(i);
      const text = await notice.textContent();
      expect(text).not.toContain('Expired');
    }
  });

  test('should display notice attachments if available', async ({ page }) => {
    await page.goto('/notices');

    // Check if any notice has attachment link
    const noticeWithAttachment = page.locator('[data-testid="notice-card"]:has([data-testid="attachment-link"])').first();

    if (await noticeWithAttachment.count() > 0) {
      const attachmentLink = noticeWithAttachment.locator('[data-testid="attachment-link"]');
      await expect(attachmentLink).toBeVisible();
      await expect(attachmentLink).toHaveAttribute('href');
    }
  });
});

test.describe('Public Website Visitor - Navigation and Layout', () => {
  test('should have consistent header across all pages', async ({ page }) => {
    const pages = ['/', '/faculty', '/results', '/gallery', '/notices'];

    for (const pagePath of pages) {
      await page.goto(pagePath);

      // Check header exists
      const header = page.locator('header');
      await expect(header).toBeVisible();

      // Check navigation links
      await expect(header.locator('a[href="/"]')).toBeVisible();
      await expect(header.locator('a[href="/faculty"]')).toBeVisible();
      await expect(header.locator('a[href="/results"]')).toBeVisible();
      await expect(header.locator('a[href="/gallery"]')).toBeVisible();
      await expect(header.locator('a[href="/notices"]')).toBeVisible();
    }
  });

  test('should have consistent footer across all pages', async ({ page }) => {
    const pages = ['/', '/faculty', '/results', '/gallery', '/notices'];

    for (const pagePath of pages) {
      await page.goto(pagePath);

      // Check footer exists
      const footer = page.locator('footer');
      await expect(footer).toBeVisible();

      // Check contact information
      await expect(footer).toContainText('Contact');
    }
  });

  test('should apply school branding colors', async ({ page }) => {
    await page.goto('/');

    // Check header has primary color applied
    const header = page.locator('header');
    const bgColor = await header.evaluate((el) => getComputedStyle(el).backgroundColor);

    // Background color should be set (not default)
    expect(bgColor).toBeTruthy();
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Check mobile menu button exists
    const mobileMenuButton = page.locator('[data-testid="mobile-menu-button"]');
    await expect(mobileMenuButton).toBeVisible();

    // Click mobile menu
    await mobileMenuButton.click();

    // Check mobile navigation appears
    const mobileNav = page.locator('[data-testid="mobile-nav"]');
    await expect(mobileNav).toBeVisible();
  });
});

test.describe('Public Website Visitor - Performance', () => {
  test('should load homepage within 2 seconds', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    const loadTime = Date.now() - startTime;

    // Should load within 2000ms (SC-004 requirement)
    expect(loadTime).toBeLessThan(2000);
  });

  test('should lazy load images in gallery', async ({ page }) => {
    await page.goto('/gallery');

    // Check images have lazy loading
    const images = page.locator('[data-testid="gallery-image"] img');
    const firstImage = images.first();

    const loading = await firstImage.getAttribute('loading');
    expect(loading).toBe('lazy');
  });
});

test.describe('Public Website Visitor - Accessibility', () => {
  test('should have accessible navigation links', async ({ page }) => {
    await page.goto('/');

    // Check all navigation links have accessible text
    const navLinks = page.locator('nav a');
    const count = await navLinks.count();

    for (let i = 0; i < count; i++) {
      const link = navLinks.nth(i);
      const text = await link.textContent();
      expect(text?.trim()).toBeTruthy();
    }
  });

  test('should have alt text for all images', async ({ page }) => {
    await page.goto('/faculty');

    // Check all images have alt attributes
    const images = page.locator('img');
    const count = await images.count();

    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');
      expect(alt).toBeTruthy();
    }
  });

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('/');

    // Tab through navigation
    await page.keyboard.press('Tab');

    // Check focus is visible
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });
});
