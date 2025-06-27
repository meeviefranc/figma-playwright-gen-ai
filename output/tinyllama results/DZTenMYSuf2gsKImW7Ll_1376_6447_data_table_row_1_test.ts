Test for Data Table_Row_1:
Elements: Rectangle 49
Generate Playwright TypeScript script:

```typescript
import { expect } from 'chai';

describe('Data Table_Row_1', () => {
  it('should have visibility', async () => {
    const table = await page.$('data-table');
    const rows = await table.getAllVisibleElements();
    expect(rows[0].getAttribute('style')).to.contain('visibility: visible;');
  });
});
```

In this test, we are using the `page` object to interact with the browser and navigate to a specific page. We then use the `await page.$('data-table')` method to locate the Data Table element. Finally, we use the `getAllVisibleElements()` method to get all the visible elements on the page. The `style` attribute of each row is checked to ensure that it has the `visibility: visible;` style property set.