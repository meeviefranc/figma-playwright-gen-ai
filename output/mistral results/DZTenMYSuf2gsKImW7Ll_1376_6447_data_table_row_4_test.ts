Here is the TypeScript code for Playwright test for "Data Table Row 4" with the specified elements:

```typescript
import { test, expect } from '@playwright/test';

test('Check Data Table Row 4', async ({ page }) => {
  // Navigate to the page
  await page.goto('your-url');

  // Select the row using data-testid selector
  const row = await page.$(`[data-testid='row-4']`);

  // Check if the row is visible and exists
  expect(row).toBeVisible();
  expect(await row.isEnabled()).toBeTruthy();

  // Select checkbox using data-testid selector
  const checkbox = await row.$(`[data-testid='checkbox']`);

  // Check if the checkbox is visible and exists
  expect(checkbox).toBeVisible();
  expect(await checkbox.isEnabled()).toBeTruthy();

  // Get text for each column using data-testid selectors
  const firstColumn = await row.$(`[data-testid='column-1']`);
  const secondColumn = await row.$(`[data-testid='column-2']`);
  const thirdColumn = await row.$(`[data-testid='column-3']`);
  const fourthColumn = await row.$(`[data-testid='column-4']`);

  // Check if the text for each column is as expected
  expect(await firstColumn.textContent()).toEqual('1');
  expect(await secondColumn.textContent()).toEqual('Kadin Herwitz');
  expect(await thirdColumn.textContent()).toEqual('Lorem ipsum dol');
  expect(await fourthColumn.textContent()).toEqual('tag');
});
```