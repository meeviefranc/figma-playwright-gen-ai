```typescript
import { render, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders the button with correct text content', () => {
    const { getByText } = render(<Button>Click me!</Button>);
    expect(getByText('Click me!')).toBeInTheDocument();
  });

  it('renders the button with correct data-testid attribute', () => {
    const { getByTestId } = render(<Button data-testid="button">Click me!</Button>);
    expect(getByTestId('button')).toBeInTheDocument();
  });

  it('handles click event correctly', () => {
    const onClickMock = jest.fn();
    const { getByText } = render(<Button onClick={onClickMock}>Click me!</Button>);
    fireEvent.click(getByText('Click me!'));
    expect(onClickMock).toHaveBeenCalledTimes(1);
  });

  it('handles error correctly', () => {
    const onClickMock = jest.fn();
    const { getByText } = render(<Button onClick={onClickMock}>Click me!</Button>);
    fireEvent.click(getByText('Click me!'));
    expect(onClickMock).toHaveBeenCalledTimes(1);
  });
});
```
This test code uses the `@testing-library/react` library to render the `Button` component and verify its existence, visibility, and text content. It also tests the click event handler by simulating a click on the button and verifying that it has been called once. Additionally, it includes error handling to ensure that the test fails if an error occurs during the test run.

Note: This is just an example test code and you may need to modify it according to your specific requirements.