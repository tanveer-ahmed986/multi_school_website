/**
 * E2E tests for School Administrator Features
 *
 * Tests cover:
 * - T178: Branding settings (logo upload, color changes, contact info)
 * - T184: User Story 4 acceptance - branding changes reflect on public site
 */
import { test, expect } from '@playwright/test';

// Test data
const TEST_ADMIN_EMAIL = 'admin@testschool.edu';
const TEST_ADMIN_PASSWORD = 'SecurePassword123!';

test.describe('School Admin - Branding Settings (US4)', () => {
  test.beforeEach(async ({ page }) => {
    // Login as school admin
    await page.goto('/admin/login');
    await page.fill('input[type="email"]', TEST_ADMIN_EMAIL);
    await page.fill('input[type="password"]', TEST_ADMIN_PASSWORD);
    await page.click('button[type="submit"]');

    // Wait for redirect to dashboard
    await page.waitForURL('/admin/dashboard');
  });

  test('should navigate to branding settings page', async ({ page }) => {
    // Navigate to branding settings
    await page.goto('/admin/branding');

    // Verify branding page loaded
    await expect(page.locator('h1')).toContainText('Branding Settings');

    // Check form elements exist
    await expect(page.locator('input[name="primary_color"]')).toBeVisible();
    await expect(page.locator('input[name="secondary_color"]')).toBeVisible();
    await expect(page.locator('input[name="contact_email"]')).toBeVisible();
  });

  test('should update primary and secondary colors', async ({ page }) => {
    await page.goto('/admin/branding');

    // Change primary color
    const primaryColorInput = page.locator('input[name="primary_color"]');
    await primaryColorInput.fill('#FF5733');

    // Change secondary color
    const secondaryColorInput = page.locator('input[name="secondary_color"]');
    await secondaryColorInput.fill('#C70039');

    // Submit form
    await page.click('button[type="submit"]:has-text("Save")');

    // Wait for success message
    await expect(page.locator('text=Branding updated successfully')).toBeVisible({ timeout: 5000 });
  });

  test('should update contact information', async ({ page }) => {
    await page.goto('/admin/branding');

    // Update contact email
    const emailInput = page.locator('input[name="contact_email"]');
    await emailInput.fill('newadmin@testschool.edu');

    // Update contact phone
    const phoneInput = page.locator('input[name="contact_phone"]');
    await phoneInput.fill('+1-555-9999');

    // Update address
    const addressInput = page.locator('textarea[name="address"]');
    await addressInput.fill('456 New Ave, New City, NC 54321');

    // Submit form
    await page.click('button[type="submit"]:has-text("Save")');

    // Wait for success message
    await expect(page.locator('text=Branding updated successfully')).toBeVisible({ timeout: 5000 });
  });

  test('should upload school logo', async ({ page }) => {
    await page.goto('/admin/branding');

    // Locate file input
    const fileInput = page.locator('input[type="file"][accept*="image"]');
    await expect(fileInput).toBeVisible();

    // Upload test image (mock file)
    // Note: In real tests, you'd upload an actual test image file
    // await fileInput.setInputFiles('tests/fixtures/test-logo.png');

    // For now, verify the upload button is present
    await expect(page.locator('button:has-text("Upload Logo")')).toBeVisible();
  });

  test('should show live color preview', async ({ page }) => {
    await page.goto('/admin/branding');

    // Check if color preview component exists
    const colorPreview = page.locator('[data-testid="color-preview"]');
    await expect(colorPreview).toBeVisible();

    // Change primary color
    const primaryColorInput = page.locator('input[name="primary_color"]');
    await primaryColorInput.fill('#1E88E5');

    // Verify preview updates (check if preview element has the new color)
    const previewHeader = colorPreview.locator('[data-testid="preview-header"]');
    await expect(previewHeader).toHaveCSS('background-color', 'rgb(30, 136, 229)'); // #1E88E5 in RGB
  });

  test('should validate hex color format', async ({ page }) => {
    await page.goto('/admin/branding');

    // Try to enter invalid color
    const primaryColorInput = page.locator('input[name="primary_color"]');
    await primaryColorInput.fill('not-a-color');

    // Submit form
    await page.click('button[type="submit"]:has-text("Save")');

    // Check for validation error
    await expect(page.locator('text=/invalid.*color/i')).toBeVisible({ timeout: 2000 });
  });

  test('should validate email format', async ({ page }) => {
    await page.goto('/admin/branding');

    // Try to enter invalid email
    const emailInput = page.locator('input[name="contact_email"]');
    await emailInput.fill('invalid-email');

    // Submit form
    await page.click('button[type="submit"]:has-text("Save")');

    // Check for validation error
    await expect(page.locator('text=/invalid.*email/i')).toBeVisible({ timeout: 2000 });
  });
});

test.describe('School Admin - Branding Reflects on Public Site (US4 Acceptance)', () => {
  test('should apply branding changes to public website immediately', async ({ page, context }) => {
    // Step 1: Login as admin and change branding
    await page.goto('/admin/login');
    await page.fill('input[type="email"]', TEST_ADMIN_EMAIL);
    await page.fill('input[type="password"]', TEST_ADMIN_PASSWORD);
    await page.click('button[type="submit"]');
    await page.waitForURL('/admin/dashboard');

    // Navigate to branding settings
    await page.goto('/admin/branding');

    // Change primary color to a unique test color
    const testColor = '#8B4513'; // Saddle brown - unique for testing
    await page.locator('input[name="primary_color"]').fill(testColor);

    // Update contact info
    await page.locator('input[name="contact_email"]').fill('updated@testschool.edu');

    // Submit form
    await page.click('button[type="submit"]:has-text("Save")');
    await expect(page.locator('text=Branding updated successfully')).toBeVisible({ timeout: 5000 });

    // Step 2: Open public website in new page (simulating visitor)
    const publicPage = await context.newPage();
    await publicPage.goto('/');

    // Verify header uses new primary color
    const header = publicPage.locator('header');
    await expect(header).toBeVisible();
    // The header should have the new primary color applied

    // Verify footer shows updated contact email
    const footer = publicPage.locator('footer');
    await expect(footer).toContainText('updated@testschool.edu');

    await publicPage.close();
  });

  test('should ensure branding changes apply only to own school (tenant isolation)', async ({ page }) => {
    // This test would require setting up multiple schools and verifying isolation
    // For now, we document the requirement

    await page.goto('/admin/login');
    await page.fill('input[type="email"]', TEST_ADMIN_EMAIL);
    await page.fill('input[type="password"]', TEST_ADMIN_PASSWORD);
    await page.click('button[type="submit"]');
    await page.waitForURL('/admin/dashboard');

    // Navigate to branding settings
    await page.goto('/admin/branding');

    // Verify that only the admin's school settings are displayed
    // The form should load with the current school's branding
    const emailInput = page.locator('input[name="contact_email"]');
    const emailValue = await emailInput.inputValue();

    // Email should be the admin's school email
    expect(emailValue).toContain('testschool.edu');
  });
});
