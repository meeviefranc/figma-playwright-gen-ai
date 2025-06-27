```markdown
# Functional Test Case for Frame 844 - Rows per page dropdown

## Preconditions
1. Navigate to the application where Frame 844 is located.
2. Ensure that the user is logged in with appropriate permissions.

## Test Steps
1. Locate the "Rows per page" dropdown within Frame 844.
2. Verify the visibility of the dropdown by checking if it's present on the screen.
3. Check the default value of the dropdown. Expected result: The default value should be '10'.
4. Select a different value from the dropdown, for example, '25'.
5. Verify that the selected value is saved and applied to the current view. Expected result: The number of rows displayed per page should change to '25'.
6. Repeat step 4 with another value, for example, '50'.
7. Verify that the selected value is saved and applied to the current view. Expected result: The number of rows displayed per page should change to '50'.
8. Verify that the dropdown still contains the original values (10, 25, 50).
9. Select the default value again ('10').
10. Verify that the selected value is saved and applied to the current view. Expected result: The number of rows displayed per page should change back to '10'.

## Expected Results
- The "Rows per page" dropdown should be visible within Frame 844.
- The default value of the dropdown should be '10'.
- Changing the value and selecting a different number (25 or 50) should correctly apply that number to the current view.
- The dropdown should contain the original values (10, 25, 50).
- Returning to the default value ('10') should correctly apply that number to the current view.
```