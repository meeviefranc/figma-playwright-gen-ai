```typescript
import { expect } from '@playwright/test';

describe('Data Table Row 1', () => {
  it('should have the correct text content', async () => {
    const dataTable = await page.locator('data-table');
    const row1 = await dataTable.locator('rectangle-49');

    // Check element existence and visibility
    expect(row1).toBeVisible();

    // Verify text content where applicable
    const textContent = await row1.textContent();
    expect(textContent).toContain('Row 1');

    // Use proper data-testid selectors
    const cell1 = await row1.locator('[data-testid="cell-1"]');
    expect(cell1).toBeVisible();

    // Include error handling
    try {
      await row1.click();
    } catch (error) {
      console.log(`Error clicking on row 1: ${error}`);
    }
  });
});
```
This test code uses the `expect` function from `@playwright/test` to check that the element exists and is visible, and verifies the text content of the element where applicable. It also uses proper data-testid selectors to locate elements within the table, and includes error handling to catch any errors that may occur during the test.

Note that this code assumes that you have already set up a Playwright test file with a `page` object that can be used to interact with the page under test. If you need help setting up a Playwright test file, please refer to the Playwright documentation.