Test for Data Table_Row_2:
Elements: button, filter, input

Generate Playwright TypeScript script to check the visibility of these elements:

```typescript
import * as React from 'react';
import { render } from 'react-dom';
import { createPortal } from 'react-dom';

const Test = () => {
  const button = document.querySelector('button');
  const filter = document.querySelector('input[type="search"]');
  const input = document.querySelector('input');

  return (
    <div>
      <h2>Data Table Row 2</h2>
      <div className="row">
        <button type="button" onClick={() => button.click()}>Filter</button>
        <input type="search" placeholder="Search..." />
      </div>
      <div className="row">
        {filter && (
          <label htmlFor="filter-input">
            Filter:{' '}
            <input id="filter-input" type="text" value={filter.value} onChange={e => filter.value = e.target.value} />
          </label>
        )}
        {input && (
          <label htmlFor="input-search">
            Search:{' '}
            <input id="input-search" type="text" value={input.value} onChange={e => input.value = e.target.value} />
          </label>
        )}
      </div>
    </div>
  );
};

const App = () => {
  return (
    <div className="container">
      <Test />
    </div>
  );
};

render(<App />, document.body);