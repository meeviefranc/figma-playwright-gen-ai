Here is a TypeScript code snippet using Playwright Test for the element named "Customer" in the Data Table Row 3. This test checks the visibility, existence, and verifies the text of the element using data-testid selectors.

```typescript
import { test, expect } from '@playwright/test';

test('Check Customer element visibility and text', async ({ page }) => {
  // Navigate to the page
  await page.goto('YOUR_URL');

  // Select the Customer element using data-testid selector
  const customerElement = await page.$(`[data-testid="Customer"]`);

  // Check if the element exists and is visible
  expect(customerElement).toBeVisible();
  expect(customerElement).toBeTruthy();

  // Verify the text of the Customer element
  const customerText = await customerElement.textContent();
  expect(customerText).toEqual('Expected Customer Text');
});
```