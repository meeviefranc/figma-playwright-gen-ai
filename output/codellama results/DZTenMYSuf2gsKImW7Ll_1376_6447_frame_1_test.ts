```typescript
import { TestFixture, Test, Page } from '@playwright/test';

@TestFixture()
class Frame1Tests {
  @Test()
  async verifyElementsExistAndAreVisible(page: Page) {
    // Check if checkbox exists and is visible
    await page.waitForSelector('[data-testid="checkbox"]');
    const checkbox = await page.$('[data-testid="checkbox"]');
    expect(checkbox).toBeTruthy();
    expect(await checkbox.isVisible()).toBe(true);

    // Check if column header exists and is visible
    await page.waitForSelector('[data-testid="column-header"]');
    const columnHeader = await page.$('[data-testid="column-header"]');
    expect(columnHeader).toBeTruthy();
    expect(await columnHeader.isVisible()).toBe(true);

    // Check if name exists and is visible
    await page.waitForSelector('[data-testid="name"]');
    const name = await page.$('[data-testid="name"]');
    expect(name).toBeTruthy();
    expect(await name.isVisible()).toBe(true);

    // Check if column sorting exists and is visible
    await page.waitForSelector('[data-testid="column-sorting"]');
    const columnSorting = await page.$('[data-testid="column-sorting"]');
    expect(columnSorting).toBeTruthy();
    expect(await columnSorting.isVisible()).toBe(true);
  }

  @Test()
  async verifyTextContentWhereApplicable(page: Page) {
    // Check if checkbox text content is correct
    const checkbox = await page.$('[data-testid="checkbox"]');
    expect(await checkbox.textContent()).toBe('Checkbox');

    // Check if column header text content is correct
    const columnHeader = await page.$('[data-testid="column-header"]');
    expect(await columnHeader.textContent()).toBe('Column Header');

    // Check if name text content is correct
    const name = await page.$('[data-testid="name"]');
    expect(await name.textContent()).toBe('Name');

    // Check if column sorting text content is correct
    const columnSorting = await page.$('[data-testid="column-sorting"]');
    expect(await columnSorting.textContent()).toBe('Column Sorting');
  }
}
```
This test fi