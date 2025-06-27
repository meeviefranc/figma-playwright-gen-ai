Here is a TypeScript code snippet using Playwright Test to interact with the element identified as "Data Table Row 1" (assuming it has a `data-testid` attribute):

```typescript
import { test, expect } from '@playwright/test';

test('Check visibility and existence of Data Table Row 1', async ({ page }) => {
  // Navigate to the page
  await page.goto('http://your-url.com');

  // Select the element using data-testid selector
  const dataTableRow1 = await page.$(`[data-testid="Data Table_Row_1"]`);

  // Check if the element exists
  expect(dataTableRow1).toBeTruthy();

  // Check if the element is visible
  await expect(dataTableRow1).toBeVisible();

  // Verify the text within the rectangle (assuming it's a child of Data Table Row 1)
  const rectangle = await dataTableRow1.$(`rect[x="49"]`);
  const textInRectangle = await rectangle.textContent();
  expect(textInRectangle).toEqual('Expected Text'); // Replace with the expected text within the rectangle
});
```