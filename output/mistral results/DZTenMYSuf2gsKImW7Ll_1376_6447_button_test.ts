Here's a simple TypeScript example using Playwright Test for the given elements: `left`, `Button` and `right`. This test checks the visibility, existence, and text of the `Button` element.

```typescript
import { test, expect } from '@playwright/test';

test('Check Button visibility, existence, and text', async ({ page }) => {
  // Navigate to the target page
  await page.goto('http://your-target-url.com');

  // Select elements using data-testid selectors
  const leftElement = page.getByTestId('left');
  const buttonElement = page.getByTestId('Button');
  const rightElement = page.getByTestId('right');

  // Check visibility and existence of the elements
  await expect(leftElement).toBeVisible();
  await expect(buttonElement).toBeVisible();
  await expect(rightElement).toBeVisible();

  // Verify the text of the Button element
  const buttonText = await buttonElement.textContent();
  await expect(buttonText).toEqual('Expected Button Text');
});
```