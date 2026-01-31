# Accessibility Testing Guide (T202)

## WCAG 2.1 Level AA Compliance

This project targets **WCAG 2.1 Level AA** compliance to ensure the platform is accessible to all users, including those with disabilities.

## Accessibility Features Implemented

### ✅ Completed (T196-T201)

1. **ARIA Labels** (T196)
   - All interactive elements have proper `aria-label` attributes
   - Forms use `aria-describedby` for error messages
   - Navigation uses `role="navigation"` and `aria-label`
   - Buttons have descriptive labels

2. **Keyboard Navigation** (T197)
   - All interactive elements are keyboard accessible
   - Focus indicators visible on all focusable elements
   - Modal/dialog focus trapping implemented
   - Logical tab order maintained

3. **Contrast Ratios** (T198)
   - Minimum 4.5:1 contrast for normal text
   - Minimum 3:1 contrast for large text (18pt+)
   - Color validation utility (`utils/accessibility.ts`)
   - Automatic text color selection for backgrounds

4. **Skip to Content Links** (T199)
   - Skip navigation links for keyboard users
   - Hidden until focused
   - Implemented in `components/accessibility/SkipToContent.tsx`

5. **Alt Text for Images** (T200)
   - All images require descriptive alt text
   - Decorative images use `alt=""` or `aria-hidden="true"`
   - `AccessibleImage` component enforces best practices

6. **Focus Management** (T201)
   - Modal focus trap (`useFocusTrap` hook)
   - Focus returns to trigger element on close
   - Escape key closes modals

## Running Lighthouse Accessibility Audit

### Option 1: Chrome DevTools (Recommended)

1. Open the application in Chrome
2. Press `F12` to open DevTools
3. Navigate to the **Lighthouse** tab
4. Select **Accessibility** category only
5. Click **Analyze page load**
6. Review the report

**Target Score**: ≥95/100

### Option 2: CLI (CI/CD Integration)

Install Lighthouse CLI:
```bash
npm install -g lighthouse
```

Run audit:
```bash
lighthouse http://localhost:3000 --only-categories=accessibility --output=html --output-path=./accessibility-report.html
```

### Option 3: Automated Testing (Recommended for CI)

```bash
npm install --save-dev @axe-core/playwright
```

Example test (`tests/accessibility.spec.ts`):
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('Homepage should not have WCAG violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
```

## Common Accessibility Issues to Check

### Critical (Must Fix)

- [ ] All images have meaningful alt text
- [ ] Form inputs have associated labels
- [ ] Color contrast meets 4.5:1 minimum
- [ ] All interactive elements are keyboard accessible
- [ ] Page has proper heading hierarchy (h1 → h2 → h3)
- [ ] Focus is visible on all focusable elements

### Important (Should Fix)

- [ ] Skip to content links present
- [ ] ARIA landmarks used correctly
- [ ] Error messages announced to screen readers
- [ ] Modal/dialog focus management
- [ ] No keyboard traps (except intentional focus traps)

### Nice to Have (Enhancement)

- [ ] Reduced motion support
- [ ] High contrast mode support
- [ ] Screen reader testing (NVDA, JAWS, VoiceOver)
- [ ] Touch target size ≥44px x 44px

## Testing with Screen Readers

### Windows (NVDA - Free)
1. Download from https://www.nvaccess.org/
2. Press `Insert + Down Arrow` to enter browse mode
3. Test navigation with Tab, Arrow keys, and headings (H key)

### macOS (VoiceOver - Built-in)
1. Press `Cmd + F5` to enable VoiceOver
2. Use `Ctrl + Option + Arrow keys` to navigate
3. Test heading navigation with `Ctrl + Option + Cmd + H`

### Testing Checklist

- [ ] Navigate entire page with Tab key only
- [ ] Navigate with screen reader
- [ ] Test all forms with keyboard only
- [ ] Verify error messages are announced
- [ ] Test modals with keyboard and screen reader
- [ ] Verify images are described properly
- [ ] Test in high contrast mode (Windows)

## WCAG 2.1 Level AA Requirements

### Perceivable
- ✅ Text alternatives for non-text content
- ✅ Captions and alternatives for multimedia
- ✅ Content can be presented in different ways
- ✅ Color is not the only visual means of conveying information
- ✅ 4.5:1 contrast ratio for normal text
- ✅ 3:1 contrast ratio for large text

### Operable
- ✅ All functionality available from keyboard
- ✅ Users have enough time to read and use content
- ✅ No content that causes seizures
- ✅ Users can navigate and find content
- ✅ Multiple ways to navigate pages

### Understandable
- ✅ Text is readable and understandable
- ✅ Pages appear and operate in predictable ways
- ✅ Users are helped to avoid and correct mistakes

### Robust
- ✅ Content is compatible with assistive technologies
- ✅ Valid HTML markup
- ✅ Proper ARIA usage

## Continuous Accessibility Testing

### Pre-commit Hook
Add to `.husky/pre-commit`:
```bash
npm run lint:accessibility
```

### CI/CD Pipeline
Add to `.github/workflows/ci.yml`:
```yaml
- name: Run Accessibility Tests
  run: npm run test:accessibility
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Axe DevTools](https://www.deque.com/axe/devtools/)

## Accessibility Score Target

**Minimum Acceptable**: 95/100
**Target**: 100/100

Run Lighthouse audit regularly and fix any issues immediately.
