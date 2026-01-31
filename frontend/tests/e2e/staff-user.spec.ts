/**
 * E2E Tests: Staff User Limited Permissions (User Story 5)
 *
 * Tests staff user access restrictions:
 * - Can access notices and gallery
 * - Cannot access results or faculty
 * - Limited dashboard view
 */

import { test, expect } from '@playwright/test';

test.describe('Staff User - Limited Permissions', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to login page
    await page.goto('/admin/login');
  });

  test('T189.1: Staff user sees limited dashboard', async ({ page }) => {
    // Login as staff user
    await page.fill('input[name="email"]', 'staff@schoola.example.com');
    await page.fill('input[name="password"]', 'staff123');
    await page.click('button[type="submit"]');

    // Wait for dashboard to load
    await page.waitForURL('/admin/staff-dashboard');

    // Verify staff dashboard is displayed
    await expect(page.locator('h1')).toContainText('Staff Dashboard');

    // Verify only permitted sections are shown
    await expect(page.locator('text=Notices')).toBeVisible();
    await expect(page.locator('text=Gallery')).toBeVisible();

    // Verify restricted sections are NOT shown
    await expect(page.locator('text=Results')).not.toBeVisible();
    await expect(page.locator('text=Faculty')).not.toBeVisible();
  });

  test('T189.2: Staff user can access notices section', async ({ page }) => {
    // Login as staff user
    await page.fill('input[name="email"]', 'staff@schoola.example.com');
    await page.fill('input[name="password"]', 'staff123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/admin/staff-dashboard');

    // Navigate to notices
    await page.click('a[href="/admin/notices"]');
    await page.waitForURL('/admin/notices');

    // Verify notice editor is accessible
    await expect(page.locator('h1')).toContainText('Manage Notices');
    await expect(page.locator('button:has-text("Add Notice")')).toBeVisible();
  });

  test('T189.3: Staff user can access gallery section', async ({ page }) => {
    // Login as staff user
    await page.fill('input[name="email"]', 'staff@schoola.example.com');
    await page.fill('input[name="password"]', 'staff123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/admin/staff-dashboard');

    // Navigate to gallery
    await page.click('a[href="/admin/gallery"]');
    await page.waitForURL('/admin/gallery');

    // Verify gallery manager is accessible
    await expect(page.locator('h1')).toContainText('Manage Gallery');
    await expect(page.locator('button:has-text("Upload Image")')).toBeVisible();
  });

  test('T189.4: Staff user denied access to results section', async ({ page }) => {
    // Login as staff user
    await page.fill('input[name="email"]', 'staff@schoola.example.com');
    await page.fill('input[name="password"]', 'staff123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/admin/staff-dashboard');

    // Try to navigate directly to results page
    await page.goto('/admin/results');

    // Should be redirected to 403 or dashboard
    await expect(page.locator('text=403')).toBeVisible();
    await expect(page.locator('text=Access Denied')).toBeVisible();
  });

  test('T189.5: Staff user denied access to faculty section', async ({ page }) => {
    // Login as staff user
    await page.fill('input[name="email"]', 'staff@schoola.example.com');
    await page.fill('input[name="password"]', 'staff123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/admin/staff-dashboard');

    // Try to navigate directly to faculty page
    await page.goto('/admin/faculty');

    // Should be redirected to 403 or dashboard
    await expect(page.locator('text=403')).toBeVisible();
    await expect(page.locator('text=Access Denied')).toBeVisible();
  });

  test('T189.6: Navigation menu shows only permitted links', async ({ page }) => {
    // Login as staff user
    await page.fill('input[name="email"]', 'staff@schoola.example.com');
    await page.fill('input[name="password"]', 'staff123');
    await page.click('button[type="submit"]');

    await page.waitForURL('/admin/staff-dashboard');

    // Check navigation menu
    const nav = page.locator('nav');

    // Permitted links should be visible
    await expect(nav.locator('a[href="/admin/notices"]')).toBeVisible();
    await expect(nav.locator('a[href="/admin/gallery"]')).toBeVisible();

    // Restricted links should NOT be visible
    await expect(nav.locator('a[href="/admin/results"]')).not.toBeVisible();
    await expect(nav.locator('a[href="/admin/faculty"]')).not.toBeVisible();
  });
});
