Here's a TypeScript code for Playwright test that checks the visibility, existence, and text of the specified elements using `data-testid` selectors:

```typescript
import { test, expect } from '@playwright/test';

test('Check Default page elements', async ({ page }) => {
  // Navigate to the default page
  await page.goto('/');

  // Check visibility and existence of "Follow me on:" element
  const followMeOn = await page.$(`[data-testid="follow-me-on"]`);
  expect(followMeOn).toBeVisible();
  expect(followMeOn).toBeTruthy();

  // Check visibility and existence of Chip elements
  const chipElements = await page.querySelectorAll(`[data-testid="chip"]`);
  for (const chip of chipElements) {
    expect(chip).toBeVisible();
    expect(chip).toBeTruthy();
  }

  // Check visibility and existence of Aspen Lubin elements
  const aspenLubinElements = await page.querySelectorAll(`[data-testid="aspen-lubin"]`);
  for (const aspenLubin of aspenLubinElements) {
    expect(aspenLubin).toBeVisible();
    expect(aspenLubin).toBeTruthy();
  }

  // Verify text content of the first Chip and Aspen Lubin elements
  const firstChip = await page.querySelector(`[data-testid="chip"]:first-child`);
  const firstAspenLubin = await page.querySelector(`[data-testid="aspen-lubin"]:first-child`);
  expect(await firstChip.textContent()).toEqual('Chip');
  expect(await firstAspenLubin.textContent()).toEqual('Aspen Lubin');
});
```