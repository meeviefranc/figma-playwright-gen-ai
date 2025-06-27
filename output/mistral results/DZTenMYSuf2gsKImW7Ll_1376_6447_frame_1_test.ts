Here is a TypeScript code for Playwright tests focusing on the elements in "Frame 1": checkbox, column-header, name, column-sorting. The test includes checking visibility and existence using data-testid selectors and includes text verification.

```typescript
import { test, expect } from '@playwright/test';

const CHECKBOX_SELECTOR = '[data-testid="checkbox"]';
const COLUMN_HEADER_SELECTOR = '[data-testid="column-header"]';
const NAME_SELECTOR = '[data-testid="name"]';
const COLUMN_SORTING_SELECTOR = '[data-testid="column-sorting"]';

test('Check visibility and existence of elements in Frame 1', async ({ page }) => {
  // Navigate to the page with Frame 1
  await page.goto('http://your-url.com');

  // Check if checkbox exists and is visible
  const checkbox = await page.locator(CHECKBOX_SELECTOR);
  await expect(checkbox).toBeVisible();
  await expect(checkbox).toHaveCount(1);

  // Check if column-header exists and is visible
  const columnHeader = await page.locator(COLUMN_HEADER_SELECTOR);
  await expect(columnHeader).toBeVisible();
  await expect(columnHeader).toHaveCount(3); // Assuming there are 3 column headers in Frame 1

  // Check if name exists and is visible
  const name = await page.locator(NAME_SELECTOR);
  await expect(name).toBeVisible();
  await expect(name).toHaveCount(1);

  // Check if column-sorting exists and is visible
  const columnSorting = await page.locator(COLUMN_SORTING_SELECTOR);
  await expect(columnSorting).toBeVisible();
  await expect(columnSorting).toHaveCount(3); // Assuming there are 3 column sortings in Frame 1

  // Verify text of the first column-header, name and column-sorting elements
  const firstColumnHeader = await page.locator(COLUMN_HEADER_SELECTOR + ':first-child');
  const firstName = await page.locator(NAME_SELECTOR + ':first-child');
  const firstColumnSorting = await page.locator(COLUMN_SORTING_SELECTOR + ':first-child');

  const expectedFirstColumnHeaderText = 'Expected Column Header Text';
  const expectedFirstNameText = 'Expected Name Text';

  await expect(firstColumnHeader).toHaveText(expectedFirstColumnHeader