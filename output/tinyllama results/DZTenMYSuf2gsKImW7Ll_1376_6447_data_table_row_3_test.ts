Test for Data Table_Row_3:
Elements: Cuusto
Generate Playwright TypeScript script to check visibility of the elements in the given data table.
```typescript
describe("Data Table_Row_3", () => {
  it("should have visible elements", () => {
    // GIVEN
    const table = document.querySelectorAll(".data-table__row");
    
    // WHEN
    table.forEach((element) => {
      expect(element).toBeVisible();
    });
  });
});
```