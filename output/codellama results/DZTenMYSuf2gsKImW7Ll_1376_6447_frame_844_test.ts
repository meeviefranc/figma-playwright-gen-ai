```typescript
import { TestFixture, Test, Page } from '@playwright/test';

@TestFixture()
class Frame844Tests {
  @Test()
  async verifyElementsExistAndAreVisible(page: Page) {
    // Navigate to the page
    await page.goto('https://example.com');

    // Verify that the rows per page dropdown exists and is visible
    const rowsPerPageDropdown = await page.$('#rows-per-page');
    expect(rowsPerPageDropdown).toBeTruthy();
    expect(await rowsPerPageDropdown.isVisible()).toBe(true);

    // Verify that the down arrow exists and is visible
    const downArrow = await page.$('#down-arrow');
    expect(downArrow).toBeTruthy();
    expect(await downArrow.isVisible()).toBe(true);

    // Verify that the rows per page dropdown has the correct text content
    const rowsPerPageText = await rowsPerPageDropdown.textContent();
    expect(rowsPerPageText).toContain('10');

    // Verify that the down arrow has the correct text content
    const downArrowText = await downArrow.textContent();
    expect(downArrowText).toBe('Down');
  }
}
```
This test fixture uses the `@TestFixture` decorator to indicate that it is a test fixture class. The `@Test` decorator is used to indicate that the `verifyElementsExistAndAreVisible` method is a test method.

The test method takes a `page: Page` parameter, which is an instance of the Playwright `Page` class. This allows us to interact with the page and its elements in the test.

Inside the test method, we navigate to the page using the `goto` method, and then verify that the rows per page dropdown and down arrow exist and are visible. We also verify that the text content of these elements is correct.

The test uses the `expect` function from Jest to make assertions about the state of the page. In this case, we use it to check that the elements exist and are visible, and that their text content is correct.

Note that this test assumes that the page has a dropdown element with an ID of "rows-per-page" and a button element with an ID of "down-arrow". If your page has different IDs or structure, you will need to modify the test accordingly.